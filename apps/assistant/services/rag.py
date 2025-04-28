from django.conf import settings
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import Document
from apps.product.models import Product, Category, Reason


class ProductKnowledgeBase:
    """
    Класс для создания и управления базой знаний о продуктах
    с использованием RAG (Retrieval-Augmented Generation)
    """

    def __init__(self, api_key=None):
        """
        Инициализация базы знаний
        """
        self.api_key = api_key or settings.GOOGLE_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.vector_store = None
        self.qa_chain = None

    def generate_product_documents(self):
        """
        Генерирует документы из базы данных продуктов для индексации
        """
        documents = []

        # Получаем все продукты
        products = Product.objects.all().select_related('category', 'boycott_reason')

        for product in products:
            # Создаем документ для каждого продукта
            content = f"Имя продукта: {product.name}\n"
            content += f"Категория: {product.category.name}\n"
            content += f"Описание: {product.description}\n"

            if product.is_boycotted:
                content += "Статус: Бойкотируемый продукт\n"
                if product.boycott_reason:
                    content += f"Причина бойкота: {product.boycott_reason.title}\n"
                    content += f"Описание причины: {product.boycott_reason.description}\n"
            else:
                content += "Статус: Не бойкотируется\n"

            if product.is_kyrgyz_product:
                content += "Местное производство: Да, это продукт Кыргызстана\n"

            # Добавляем информацию об альтернативах
            alternatives = product.alternative_products.all()
            if alternatives:
                content += "Альтернативные продукты:\n"
                for alt in alternatives:
                    kyrgyz_status = "местного производства" if alt.is_kyrgyz_product else ""
                    content += f"- {alt.name} {kyrgyz_status}\n"

            # Создаем Document объект (не словарь)
            documents.append(
                Document(
                    page_content=content,
                    metadata={"id": product.id, "name": product.name}
                )
            )

        # Добавляем информацию о причинах бойкота
        reasons = Reason.objects.all()
        for reason in reasons:
            content = f"Причина бойкота: {reason.title}\n"
            content += f"Описание: {reason.description}\n"
            content += "Продукты, бойкотируемые по этой причине:\n"

            related_products = Product.objects.filter(boycott_reason=reason)
            for product in related_products:
                content += f"- {product.name}\n"

            # Создаем Document объект (не словарь)
            documents.append(
                Document(
                    page_content=content,
                    metadata={"id": f"reason_{reason.id}", "title": reason.title}
                )
            )

        return documents

    def build_knowledge_base(self):
        """
        Создает векторное хранилище и цепочку для ответа на вопросы
        """
        # Генерируем документы
        documents = self.generate_product_documents()

        # Создаем текстовые сплиттеры для разбиения документов
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        # Создаем векторное хранилище
        self.vector_store = Chroma.from_documents(
            documents=texts,
            embedding=self.embeddings,
            persist_directory="./chroma_db"
        )

        # Создаем цепочку для ответа на вопросы
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0, openai_api_key=self.api_key),
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 3})
        )

    def ask(self, question):
        """
        Задает вопрос базе знаний и получает ответ
        """
        if not self.qa_chain:
            raise ValueError("Knowledge base is not built yet. Call build_knowledge_base first.")

        # Формируем запрос с контекстом
        if "бойкот" in question.lower() and "почему" in question.lower():
            # Вопрос о причине бойкота
            query = f"Почему продукт бойкотируется? {question}"
        elif "альтернатив" in question.lower():
            # Вопрос об альтернативах
            query = f"Какие альтернативы существуют для этого продукта? {question}"
        else:
            # Общий вопрос
            query = question

        # Получаем ответ
        result = self.qa_chain.run(query)

        return result


class SimpleProductKnowledgeBase:
    """
    Простой класс для ответов на вопросы о продуктах без векторных баз и эмбеддингов.
    """

    def __init__(self):
        pass

    def find_product(self, question: str):
        """
        Ищет продукт в базе данных по тексту вопроса
        """
        products = Product.objects.all()
        for product in products:
            if product.name.lower() in question.lower():
                return product
        return None

    def build_answer(self, product: Product):
        """
        Строит текст ответа по найденному продукту
        """
        if not product:
            return "Извините, я не нашёл такой продукт. Пожалуйста, уточните название."

        response = f"🛍️ <b>Продукт:</b> {product.name}\n\n"
        response += f"📄 <b>Описание:</b> {product.description or 'Нет описания.'}\n\n"

        if product.is_boycotted:
            response += "🚫 <b>Статус:</b> Бойкотируемый продукт\n"
            if product.boycott_reason:
                response += f"❗ <b>Причина бойкота:</b> {product.boycott_reason.title}\n"
                response += f"{product.boycott_reason.description}\n\n"
        else:
            response += "✅ <b>Статус:</b> Продукт не находится под бойкотом.\n\n"

        alternatives = product.alternative_products.all()
        if alternatives.exists():
            response += "🔄 <b>Альтернативные продукты:</b>\n"
            for alt in alternatives:
                response += f"- {alt.name}\n"

        return response

    def ask(self, question: str):
        """
        Основной метод: принимает вопрос и возвращает ответ
        """
        product = self.find_product(question)
        return self.build_answer(product)

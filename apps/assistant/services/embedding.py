from typing import Any, Dict, List, Tuple

import numpy as np
from django.conf import settings
from django.db.models import Q
from openai import OpenAI

from apps.assistant.models import ProductEmbedding
from apps.product.models import Product

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class EmbeddingService:
    """Service for creating and managing embeddings"""

    @staticmethod
    def get_product_text(product: Product) -> str:
        """Generate text representation of product for embedding"""
        text = f"Name: {product.name}\n"
        text += f"Category: {product.category.name}\n"
        text += f"Description: {product.description}\n"

        if product.is_boycotted and product.boycott_reason:
            text += (
                f"This product is boycotted because: "
                f"{product.boycott_reason.title} - "
                f"{product.boycott_reason.description}\n"
            )

        if product.is_kyrgyz_product:
            text += "This is a Kyrgyz product.\n"

        # Add alternative product information
        alternatives = product.alternative_products.all()
        if alternatives.exists():
            alt_names = [alt.name for alt in alternatives]
            text += f"Alternative products: {', '.join(alt_names)}\n"

        return text

    @staticmethod
    def create_embedding(text: str) -> List[float]:
        """Create embedding vector for text using OpenAI API"""
        return client.embeddings.create(input=text, model="text-embedding-3-small").data[0].embedding

    @classmethod
    def generate_and_store_embeddings(cls) -> int:
        """Generate embeddings for all products and store them"""
        count = 0
        for product in Product.objects.all():
            text = cls.get_product_text(product)
            embedding_vector = cls.create_embedding(text)

            # Store embedding
            ProductEmbedding.objects.update_or_create(product=product, defaults={"embedding_vector": embedding_vector})
            count += 1

        return count

    @staticmethod
    def cosine_similarity(a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a_array = np.array(a)
        b_array = np.array(b)
        return np.dot(a_array, b_array) / (np.linalg.norm(a_array) * np.linalg.norm(b_array))

    @classmethod
    def semantic_search(cls, query: str, top_n: int = 5) -> List[Tuple[Product, float]]:
        """Search for products semantically similar to the query"""
        # Create embedding for query
        query_embedding = cls.create_embedding(query)

        # Get all product embeddings
        product_embeddings = ProductEmbedding.objects.all()

        # Calculate similarity scores
        similarity_scores = []
        for prod_emb in product_embeddings:
            similarity = cls.cosine_similarity(query_embedding, prod_emb.embedding_vector)
            similarity_scores.append((prod_emb.product, similarity))

        # Sort by similarity (descending)
        similarity_scores.sort(key=lambda x: x[1], reverse=True)

        # Return top N results
        return similarity_scores[:top_n]


class QueryEngine:
    """Engine for processing and responding to user queries using the product database"""

    @staticmethod
    def response_ai(query: str):
        return client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Вы - помощник по бойкоту товаров."},
                {"role": "user", "content": query},
            ],
        )

    @staticmethod
    def generate_response(query: str) -> Dict[str, Any]:
        """Generate a response to a user query"""
        # First, try keyword search
        keyword_results = QueryEngine._keyword_search(query)

        # Then do semantic search
        semantic_results = EmbeddingService.semantic_search(query, top_n=3)

        # Combine results, prioritizing keyword matches but including semantic matches
        all_products = set()
        results = []

        # Add keyword results first
        for product in keyword_results:
            if product.id not in all_products:
                results.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "category": product.category.name,
                        "is_boycotted": product.is_boycotted,
                        "boycott_reason": (
                            product.boycott_reason.title if product.is_boycotted and product.boycott_reason else None
                        ),
                        "is_kyrgyz_product": product.is_kyrgyz_product,
                        "rating": product.get_rating(),
                        "match_type": "keyword",
                    }
                )
                all_products.add(product.id)

        # Then add semantic results
        for product, similarity in semantic_results:
            if product.id not in all_products:
                results.append(
                    {
                        "id": product.id,
                        "name": product.name,
                        "category": product.category.name,
                        "is_boycotted": product.is_boycotted,
                        "boycott_reason": (
                            product.boycott_reason.title if product.is_boycotted and product.boycott_reason else None
                        ),
                        "is_kyrgyz_product": product.is_kyrgyz_product,
                        "rating": product.get_rating(),
                        "match_type": "semantic",
                        "similarity": similarity,
                    }
                )
                all_products.add(product.id)

        # Get the top product
        top_product = None
        if results:
            top_product = results[0]

            # Increment query count for top product
            product = Product.objects.get(id=top_product["id"])
            product.query_count += 1
            product.save()

        # Generate natural language response
        response_text = QueryEngine._create_response_text(query, results)

        return {"query": query, "results": results, "response_text": response_text}

    @staticmethod
    def _keyword_search(query: str) -> List[Product]:
        """Perform keyword-based search on products"""
        # Clean and normalize the query
        query_terms = query.lower().split()

        # Search in product names, descriptions, and categories
        q_objects = Q()
        for term in query_terms:
            q_objects |= Q(name__icontains=term) | Q(description__icontains=term) | Q(category__name__icontains=term)

        # Special query terms
        if "boycott" in query_terms or "boycotted" in query_terms:
            q_objects |= Q(is_boycotted=True)

        if "kyrgyz" in query_terms:
            q_objects |= Q(is_kyrgyz_product=True)

        return Product.objects.filter(q_objects).distinct()[:5]

    @staticmethod
    def _create_response_text(query: str, results: List[Dict[str, Any]]) -> str:
        """Create a natural language response based on query and results"""
        if not results:
            return f"I couldn't find any products matching '{query}'. Could you try a different search term?"

        top_product = results[0]

        response = f"For your query '{query}', I found {len(results)} matching products. "

        # Detailed info about top result
        response += f"The best match is '{top_product['name']}' in the {top_product['category']} category. "

        if top_product["is_boycotted"]:
            response += f"This product is being boycotted due to: {top_product['boycott_reason']}. "

            # Suggest alternatives if this product is boycotted
            alternatives = Product.objects.filter(alternative_products__id=top_product["id"], is_boycotted=False)
            if alternatives.exists():
                alt_names = [alt.name for alt in alternatives[:3]]
                response += f"You might consider these alternatives: {', '.join(alt_names)}. "

        if top_product["is_kyrgyz_product"]:
            response += "This is a Kyrgyz product. "

        response += f"It has a rating of {top_product['rating']} out of 5. "

        # Add info about other matches if available
        if len(results) > 1:
            other_products = [r["name"] for r in results[1:]]
            response += f"I also found these other products that might interest you: {', '.join(other_products)}."

        return response

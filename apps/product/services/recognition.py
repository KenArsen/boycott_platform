# import cv2
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
# from tensorflow.keras.preprocessing import image
#
# from apps.product.models import Product
#
#
# def load_model():
#     """Загрузка предобученной модели для распознавания изображений"""
#     # Вы можете использовать предобученную модель или свою собственную
#     model = MobileNetV2(weights="imagenet")
#     return model
#
#
# # Глобальная переменная для модели, чтобы не загружать ее каждый раз
# RECOGNITION_MODEL = None
#
#
# def get_recognition_model():
#     """Получение экземпляра модели"""
#     global RECOGNITION_MODEL
#     if RECOGNITION_MODEL is None:
#         RECOGNITION_MODEL = load_model()
#     return RECOGNITION_MODEL
#
#
# def preprocess_image(img_path):
#     """Предобработка изображения для модели"""
#     img = image.load_img(img_path, target_size=(224, 224))
#     x = image.img_to_array(img)
#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)
#     return x
#
#
# def recognize_product(img_path):
#     """Распознавание продукта на изображении"""
#     model = get_recognition_model()
#
#     # Предобработка изображения
#     img_tensor = preprocess_image(img_path)
#
#     # Получение предсказаний
#     predictions = model.predict(img_tensor)
#     results = decode_predictions(predictions, top=3)[0]
#
#     # Преобразование результатов
#     recognition_results = []
#     for _, label, confidence in results:
#         # Преобразуем метку в более читаемый формат
#         label = label.replace("_", " ").title()
#         recognition_results.append({"label": label, "confidence": float(confidence)})
#
#     return recognition_results
#
#
# def find_matching_products(recognition_results):
#     """Поиск соответствующих продуктов в базе данных по результатам распознавания"""
#     matching_products = []
#
#     for result in recognition_results:
#         # Ищем продукты по названию или ключевым словам
#         products = Product.objects.filter(name__icontains=result["label"])
#
#         if products.exists():
#             for product in products:
#                 # Увеличиваем счетчик запросов
#                 product.query_count += 1
#                 product.save()
#
#                 matching_products.append(
#                     {
#                         "id": product.id,
#                         "name": product.name,
#                         "description": product.description,
#                         "category": product.category.name,
#                         "is_boycotted": product.is_boycotted,
#                         "boycott_reason": product.boycott_reason.name if product.boycott_reason else None,
#                         "is_kyrgyz_product": product.is_kyrgyz_product,
#                         "image_url": product.image.url if product.image else None,
#                         "rating": product.get_rating(),
#                         "confidence": result["confidence"],
#                     }
#                 )
#
#     return matching_products

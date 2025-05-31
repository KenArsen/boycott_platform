from django.urls import path

from apps.assistant.views.about_us import about_us
from apps.assistant.views.boycott_asistant import chatbot_ui, search_product_api
from apps.assistant.views.contact import contact

app_name = "assistant"

urlpatterns = [
    path("", chatbot_ui, name="chatbot-ui"),
    path("search-product/", search_product_api, name="search-product-api"),
    path("about-us/", about_us, name="about-us"),
    path("contact/", contact, name="contact"),
]

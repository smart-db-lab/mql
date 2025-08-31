"""
URL configuration for dl4ml project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path,include
from django.conf.urls.static import static


from backend_app.views import *
# def hi(request):
#     return HttpResponse("<div><p>hi</p></div>")


urlpatterns = [
    # path('',lambda request: render(request, 'hi.html')),
    # path('',hi),
    
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/', include('backend_app.urls')),
    # path('upload_file/', upload)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






# import torch
# from transformers import AutoTokenizer, AutoModel
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# # Load BERT tokenizer and model
# tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
# model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# # List of FAQs
# faq_responses = {
#     "What is your return policy?": "Our return policy allows you to return items within 30 days of purchase.",
#     "How long does shipping take?": "Shipping usually takes 5-7 business days depending on your location.",
#     "What payment methods do you accept?": "We accept credit cards, PayPal, and bank transfers."
# }

# # Function to get sentence embeddings using BERT
# def get_embeddings(sentences):
#     inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
#     outputs = model(**inputs)
#     return outputs.last_hidden_state.mean(dim=1).detach().numpy()

# # Function to find the most similar FAQ based on the user question
# def find_closest_faq(user_question):
#     faq_questions = list(faq_responses.keys())
#     question_embeddings = get_embeddings(faq_questions)
#     user_embedding = get_embeddings([user_question])

#     # Calculate cosine similarity
#     similarities = cosine_similarity(user_embedding, question_embeddings).flatten()

#     # Get the index of the most similar FAQ
#     closest_index = np.argmax(similarities)
#     return faq_questions[closest_index], similarities[closest_index]

# # Example: Compare user question with FAQs
# user_question = "Can I return an item?"
# closest_faq, similarity_score = find_closest_faq(user_question)

# if similarity_score > 0.7:  # You can set a similarity threshold
#     print(f"Matched FAQ: {closest_faq}")
#     print(f"Response: {faq_responses[closest_faq]}")
# else:
#     print("No similar FAQ found, forwarding the question to the chatbot.")

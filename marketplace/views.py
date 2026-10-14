from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Item, Category, Review
from .forms import ItemForm, ReviewForm

class HomeView(ListView):
    model = Item
    template_name = 'marketplace/home.html'
    context_object_name = 'items'
    paginate_by = 12
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'marketplace/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        if self.request.user.is_authenticated:
            context['user_review'] = self.object.reviews.filter(reviewer=self.request.user).first()
        return context

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'marketplace/item_form.html'
    success_url = reverse_lazy('marketplace:home')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'marketplace/item_form.html'

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.seller

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('marketplace:home')
    template_name = 'marketplace/item_confirm_delete.html'

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.seller

class CategoryDetailView(ListView):
    model = Item
    template_name = 'marketplace/category_detail.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Item.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        # Provide categories for the sidebar (same as HomeView)
        context['categories'] = Category.objects.all()
        return context

class ItemSearchView(ListView):
    model = Item
    template_name = 'marketplace/search_results.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Item.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        return Item.objects.none()

class MyListingsView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'marketplace/my_listings.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        return Item.objects.filter(seller=self.request.user).order_by('-created_at')

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'marketplace/review_form.html'

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.item = get_object_or_404(Item, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('marketplace:item-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Provide the item object to the template so item.pk is available for links/cancel
        context['item'] = get_object_or_404(Item, pk=self.kwargs.get('pk'))
        return context

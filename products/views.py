from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from carts.models import Cart
from .models import Product

class ProductFeaturedListView(ListView):
	template_name = "products/list.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
	template_name = "products/featured-detail.html"

	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all().featured()
	

class ProductListView(ListView):
	
	template_name = "products/list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context

	def get_context_data(self, *args, **kwargs):
		# *args (arg, arg, arg,...) 
		# **kwargs (keyword=arg, keyword=arg,..)
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		print(context)
		return context

	def get_queryset(self, *args, **kwargs):
		# defined fuction to replace queryset = Product.objects.all()
		request = self.request
		return Product.objects.all()

# same as above
def product_list_view(request):
	queryset = Product.objects.all()
	context = {
		'object_list': queryset
	}
	return render(request, "products/list.html", context)



class ProductDetailView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		print(context)
		return context
	
	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance == None:
			raise Http404("Product doesn't exist. Please check your product index again.")
		return instance
	
	# def get_queryset(self, *args, **kwargs):
	# 	# same result as get_object
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)

# same as above
def product_detail_view(request, pk=None, *args, **kwargs):
	# instance = Product.objects.get(pk=pk) # primary key, id
	#instance = get_object_or_404(Product, pk=pk)
	# try:
	# 	instance = Product.objects.get(id=pk)
	# except Product.DoesNotExist:
	# 	print('nothing for this product index')
	# 	raise Http404("Product doesn't exist. Please check your product index again.")
	# except:
	# 	print('there is an error looking this product index')
	
	instance = Product.objects.get_by_id(pk)
	if instance == None:
		raise Http404("Product doesn't exist. Please check your product index again.")
	# use customized Model Manager to replace the following
	# qs = Product.objects.filter(id=pk)
	# if qs.exist() and qs.count() == 1:
	# 	instance = qs.first()
	# else:
	# 	raise Http404("Product doesn't exist. Please check your product index again.")

	context = {
		'object': instance
	}
	return render(request, "products/detail.html", context)

class ProductDetailSlugView(DetailView):
	queryset = Product.objects.all()
	template_name = "products/detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(self.request)
		context['cart'] = cart_obj
		return context
	
	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		try:
			instance = get_object_or_404(Product, slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404("Product doesn't exist. Please check your product index again.")
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404("check the code.")
		return instance
from django import forms
from django.core.files.base import ContentFile
from slugify import slugify
import urllib2
# from urllib import request

from .models import Image

class ImageForm(forms.ModelForm):
    class  Meta:
        model = Image
        fields = ('title','url','description')
    
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png']
        extension = url.rsplit(".",1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("The given Url does not match valid image extension")
        return url

    def save(self,force_insert=False,force_update=False,commit=True):
        image = super(ImageForm,self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{0}.{1}'.format(slugify(image.title),image_url.rsplit('.',1)[1].lower())
        # response = request.urlopen(image_url)

        proxy_info = [
            "http://softupdate:update20161214@10.10.1.7:18263",
            "https://softupdate:update20161214@10.10.1.7:18263",
            "http://berg:9608769171@10.10.1.77:18263"
        ]
        prosy_support = urllib2.ProxyHandler({"https":proxy_info[1],"http":proxy_info[0]})
        opener = urllib2.build_opener(prosy_support)
        urllib2.install_opener(opener)

        req = urllib2.Request(image_url)
        response = urllib2.urlopen(req)
        image.image.save(image_name,ContentFile(response.read()),save=False)
        if commit:
            image.save()
        return image

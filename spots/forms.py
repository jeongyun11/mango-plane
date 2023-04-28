from django import forms
from .models import Spot, Comment


class SpotForm(forms.ModelForm):
    title = forms.CharField(
        label='여행지',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style': 'width: 250px',
            }
        ),
    )
    content = forms.CharField(
        label='내용',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'style': 'width: 250px',
            }
        ),
    )
    address = forms.CharField(
        label='주소',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
            }
        ),
    )
    phone_number = forms.CharField(
        label='전화번호',
        empty_value='전화번호를 입력해주세요',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
            }
        ),
    )
    price_range = forms.CharField(
        label='가격대',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
            }
        ),
    )
    parking = forms.BooleanField(
        label='주차 가능 여부',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        ),
    )
    business_hours = forms.CharField(
        label='영업시간',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
            }
        ),
    )
    holiday = forms.DateField(
        label='휴무일',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'style' : 'width: 250px',
            }
        ),
    )
    website = forms.URLField(
        label='웹사이트',
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
            }
        ),
    )

    class Meta:
        model = Spot
        fields = ('title', 'content', 'image', 'category', 'address', 'phone_number', 'price_range', 'parking', 'business_hours', 'holiday', 'website',)
        labels = {
            'image': '이미지',
            'category': '카테고리',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'image')
        widgets = {'content': forms.TextInput}

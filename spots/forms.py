from django import forms
from .models import Spot, Comment, CommentImage
from django.forms import formset_factory
from django.contrib.auth import get_user_model

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
    category = forms.CharField(
        label='카테고리',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
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
                'id' : 'address_kakao',
            }
        ),
    )
    price_range = forms.CharField(
        label='가격대',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'style' : 'width: 250px',
                'name' : 'charge',
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
        fields = ('title', 'content', 'image', 'category', 'address', 'price_range', 'parking', 'website',)
        labels = {
            'image': '이미지',

        }


class CommentForm(forms.ModelForm):
    vote = forms.ChoiceField(choices=Comment.VOTE_CHOICES)
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={
            'class': 'ReviewEditor__Editor',
            'maxlength': '10000',
            'style': 'overflow: hidden; overflow-wrap: break-word; width: 644px; height: 150px; border: 1px solid #DBDBDB;',
        }),
    )
    vote = forms.ChoiceField(
        label='',
        choices=Comment.VOTE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'emojiFlex',
            'style': 'display: none;',
            'onclick': "var radio = document.getElementsByName('vote');\
                        for (var i=0; i<radio.length; i++) {\
                            if (radio[i].checked) {\
                                radio[i].parentNode.style.color='#ff9008';\
                                radio[i].parentNode.querySelector('.EmoticonPicker__Icon').style.color = '#ff9008';\
                            } else {\
                                radio[i].parentNode.style.color='#959595';\
                                radio[i].parentNode.querySelector('.EmoticonPicker__Icon').style.color = '#959595';\
                            }\
                        }"
        }),
    )

    class Meta:
        model = Comment
        fields = ('vote', 'content')  # 'image'를 제거합니다.

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        spot = kwargs.pop('spot')  # spot 인자를 받아옵니다.
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request:
            self.fields['content'].widget.attrs['placeholder'] = f"{self.request.user}님, 이번 여행은 어떠셨나요? 여행지의 분위기와 후기가 궁금해요!"
    
    def clean_vote(self):
        vote = self.cleaned_data.get('vote')
        return float(vote)
        
class CommentImageForm(forms.ModelForm):
    class Meta:
        model = CommentImage
        fields = ('image',)

CommentImageFormSet = forms.formset_factory(CommentImageForm, extra=1, max_num=30)

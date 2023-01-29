from django import forms
from .models import Topic, AnswerComment, Answer, Question, QuestionComment, Vote, Like


class FormAnswer(forms.ModelForm):
	class Meta:
		model = Answer

		fields = '__all__'

class FormTopic(forms.ModelForm):
	class Meta:
		model = Topic

		fields = '__all__'

class FormQuestion(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('question','description','keywords','topic')

	def __init__(self, *args, **kwargs):
		super(FormQuestion,self).__init__(*args,**kwargs)
		field = ('question','description','keywords')
		for i in self.fields:
			if i in field:
				self.fields[i].widget.attrs['class'] = 'form-control mb-2'
				self.fields[i].widget.attrs['rows'] = 4
			else:
				self.fields[i] = forms.ModelMultipleChoiceField(
				queryset=Topic.objects.all(),
				widget=forms.CheckboxSelectMultiple
				)
				self.fields[i].widget.attrs['class'] = 'mb-2'
					
class FormQuestionComment(forms.ModelForm):
	class Meta:
		model = QuestionComment

		fields = '__all__'

class FormAnswerComment(forms.ModelForm):
	class Meta:
		model = AnswerComment

		fields = '__all__'

class FormVote(forms.ModelForm):
	class Meta:
		model = Vote

		fields = '__all__'

class FormLike(forms.ModelForm):
	class Meta:
		model = Like

		fields = '__all__'


from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django_weasyprint import WeasyTemplateView

from digits.core import forms, models


@login_required
def home(request):
    aprs_qty = models.PreliminaryRiskAnalysis.objects.all().count()
    return render(request, 'home.html', {'aprs_qty': aprs_qty})


@login_required
def apr_list(request):
    user = request.user
    company = user.selected_company
    aprs = models.PreliminaryRiskAnalysis.objects.filter(
        company=company
    )
    context = {
        'apr_list': aprs
    }
    return render(request, 'core/apr_list.html', context)


@login_required
def apr_new(request):
    accident_risk_questions = models.DefaultRiskQuestion.objects.filter(
        default_risk_analysis__id=1, 
        risk_question__category=models.RiskQuestion.ACCIDENT
    )
    AccidentQuestionsFormSet = inlineformset_factory(
        models.PreliminaryRiskAnalysis, models.RiskAnswer,
        form=forms.RiskAnswerForm,
        extra=accident_risk_questions.count(),
        can_delete=False
    )

    biological_risk_questions = models.DefaultRiskQuestion.objects.filter(
        default_risk_analysis__id=1, 
        risk_question__category=models.RiskQuestion.BIOLOGICAL
    )
    BiologicalQuestionsFormSet = inlineformset_factory(
        models.PreliminaryRiskAnalysis, models.RiskAnswer,
        form=forms.RiskAnswerForm,
        extra=biological_risk_questions.count(),
        can_delete=False
    )

    physical_risk_questions = models.DefaultRiskQuestion.objects.filter(
        default_risk_analysis__id=1, 
        risk_question__category=models.RiskQuestion.PHYSICAL
    )
    PhysicalQuestionsFormSet = inlineformset_factory(
        models.PreliminaryRiskAnalysis, models.RiskAnswer,
        form=forms.RiskAnswerForm,
        extra=physical_risk_questions.count(),
        can_delete=False
    )

    chemical_risk_questions = models.DefaultRiskQuestion.objects.filter(
        default_risk_analysis__id=1,
        risk_question__category=models.RiskQuestion.CHEMICAL
    )
    ChemicalQuestionsFormSet = inlineformset_factory(
        models.PreliminaryRiskAnalysis, models.RiskAnswer,
        form=forms.RiskAnswerForm,
        extra=chemical_risk_questions.count(),
        can_delete=False
    )

    if request.method == 'POST':
        form = forms.RiskAnalysisForm(request.POST)
        accident_questions_formset = AccidentQuestionsFormSet(
            request.POST,
            initial=[{'question': rq.id} for rq in accident_risk_questions],
            prefix='accident'
        )
        biological_questions_formset = BiologicalQuestionsFormSet(
            request.POST,
            initial=[{'question': rq.id} for rq in biological_risk_questions],
            prefix='biological'
        )
        physical_questions_formset = PhysicalQuestionsFormSet(
            request.POST,
            initial=[{'question': rq.id} for rq in physical_risk_questions],
            prefix='physical'
        )
        chemical_questions_formset = ChemicalQuestionsFormSet(
            request.POST,
            initial=[{'question': rq.id} for rq in chemical_risk_questions],
            prefix='chemical'
        )
        try:
            with transaction.atomic():
                if form.is_valid():
                    valid = True
                    company = request.user.selected_company
                    apr = form.save(commit=False)
                    apr.company = company
                    apr.status = models.PreliminaryRiskAnalysis.REGISTERING
                    apr.created_by = request.user
                    apr.updated_by = request.user
                    apr.save()

                    accident_questions_formset.instance = apr
                    if accident_questions_formset.is_valid():
                        accident_questions_formset.save()
                    else:
                        valid = False

                    biological_questions_formset.instance = apr
                    if biological_questions_formset.is_valid():
                        biological_questions_formset.save()
                    else:
                        valid = False

                    physical_questions_formset.instance = apr
                    if physical_questions_formset.is_valid():
                        physical_questions_formset.save()
                    else:
                        valid = False

                    chemical_questions_formset.instance = apr
                    if chemical_questions_formset.is_valid():
                        chemical_questions_formset.save()
                    else:
                        valid = False

                    if not valid:
                        raise ValidationError('')
                    return redirect('core:apr_list')
        except (IntegrityError, ValidationError) as e:
            print(e)
            context = {
                'form': form,
                'accident_formset': accident_questions_formset,
                'biological_formset': biological_questions_formset,
                'physical_formset': physical_questions_formset,
                'chemical_formset': chemical_questions_formset,
            }
            return render(request, 'core/apr_form_general.html', context)

    form = forms.RiskAnalysisForm()
    accident_questions_formset = AccidentQuestionsFormSet(
        initial=[{'question': rq.id} for rq in accident_risk_questions],
        prefix='accident'
    )
    biological_questions_formset = BiologicalQuestionsFormSet(
        initial=[{'question': rq.id} for rq in biological_risk_questions],
        prefix='biological'
    )
    physical_questions_formset = PhysicalQuestionsFormSet(
        initial=[{'question': rq.id} for rq in physical_risk_questions],
        prefix='physical'
    )
    chemical_questions_formset = ChemicalQuestionsFormSet(
        initial=[{'question': rq.id} for rq in chemical_risk_questions],
        prefix='chemical'
    )

    context = {
        'form': form,
        'accident_formset': accident_questions_formset,
        'biological_formset': biological_questions_formset,
        'physical_formset': physical_questions_formset,
        'chemical_formset': chemical_questions_formset,
    }
    return render(request, 'core/apr_form_general.html', context)


@login_required
def apr_detail(request, pk):
    user = request.user
    company = user.selected_company
    apr = get_object_or_404(models.PreliminaryRiskAnalysis, pk=pk)
    accident_risks = apr.answers.filter(
        question__risk_question__category=models.RiskQuestion.ACCIDENT
    )
    biological_risks = apr.answers.filter(
        question__risk_question__category=models.RiskQuestion.BIOLOGICAL
    )
    physical_risks = apr.answers.filter(
        question__risk_question__category=models.RiskQuestion.PHYSICAL
    )
    chemical_risks = apr.answers.filter(
        question__risk_question__category=models.RiskQuestion.CHEMICAL
    )
    sign_form = AuthenticationForm()
    context = {
        'apr': apr,
        'accident_risks': accident_risks,
        'biological_risks': biological_risks,
        'physical_risks': physical_risks,
        'chemical_risks': chemical_risks,
        'sign_form': sign_form
    }
    return render(request, 'core/apr_detail.html', context)


@login_required
def apr_sign(request, pk):
    user = request.user
    company = user.selected_company
    apr = get_object_or_404(models.PreliminaryRiskAnalysis, pk=pk)
    sign_form = forms.SignForm(request.POST)
    if sign_form.is_valid():
        print('OK')
    return redirect('core:apr_detail', pk=apr.id)
    
    


@method_decorator(login_required, name='dispatch')
class APRDetailPDF(WeasyTemplateView):
    # pdf_stylesheets = [
    #     settings.STATIC_ROOT + '/bootstrap/css/bootstrap.min.css',
    #     settings.STATIC_ROOT + '/css/pdfFiles.css',
    # ]
    template_name = 'core/apr_detail_pdf.html'
    pdf_attachment = True
    pdf_filename = 'apr.pdf'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        apr = get_object_or_404(models.PreliminaryRiskAnalysis, pk=pk)
        accident_risks = apr.answers.filter(
            question__risk_question__category=models.RiskQuestion.ACCIDENT
        )
        biological_risks = apr.answers.filter(
            question__risk_question__category=models.RiskQuestion.BIOLOGICAL
        )
        physical_risks = apr.answers.filter(
            question__risk_question__category=models.RiskQuestion.PHYSICAL
        )
        chemical_risks = apr.answers.filter(
            question__risk_question__category=models.RiskQuestion.CHEMICAL
        )
        context = self.get_context_data(**kwargs)
        context.update({
            'apr': apr,
            'accident_risks': accident_risks,
            'biological_risks': biological_risks,
            'physical_risks': physical_risks,
            'chemical_risks': chemical_risks
        })
        return self.render_to_response(context)

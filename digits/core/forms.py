from django import forms

from digits.core import models


class RiskAnalysisForm(forms.ModelForm):
    
    class Meta:
        model = models.PreliminaryRiskAnalysis
        fields = [
            'activity_type', 'location', 'estimated_execution_time',
            'work_permission'
        ]

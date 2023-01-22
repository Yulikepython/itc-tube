import django_filters
from nippo.models import NippoModel
from django.forms.widgets import Select

public_choices = ((0, "全て"), (1, "公開済のみ"), (2, "ドラフトのみ"))

class NippoModelFilter(django_filters.FilterSet):
    #公開・非公開を入力
    public = django_filters.TypedChoiceFilter(
                        choices=public_choices, 
                        method="public_chosen", 
                        label="公開済み・下書き", 
                        widget=Select(attrs={
                                "class":"form-select"
                                    }))
    #年月日によるもの
    date = django_filters.TypedChoiceFilter(
                method="timestamp_checker", 
                label="作成月", 
                widget=Select(attrs={
                    "class":"form-select"
                }))

    class Meta:
        model = NippoModel
        fields = ["date", "public"]

    def __init__(self, *args, **kwargs):
        qs = kwargs["queryset"]
        choice_option = [(obj.date.year, obj.date.month) for obj in qs]
        choice_option = list(set(choice_option))
        choice_option.sort(reverse=True)
        DATE_OPTIONS = [
            ((year, month), f"{year}年{month}月") for year, month in choice_option
            ]
        DATE_OPTIONS.insert(0, (None, "---"))
        self.base_filters["date"].extra["choices"] = DATE_OPTIONS
        super().__init__(*args, **kwargs)

    def timestamp_checker(self, queryset, name, value):
        qs = queryset
        if value is not None:
            year, month = eval(value)
            # print(year, month)
            qs = queryset.filter(date__year=year).filter(date__month=month)
        return qs

    def public_chosen(self, queryset, name, value):
        qs = queryset
        if value == "1":#公開済み
            qs = qs.filter(public=True)
        elif value == "2":#非公開
            qs = qs.filter(public=False)
        return qs
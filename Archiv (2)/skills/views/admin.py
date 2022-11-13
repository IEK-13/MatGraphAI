from dal import autocomplete

from skills.models.skills import ESCOSkill

from neomodel import Q


class ESCOSkillAutocompleteView(autocomplete.Select2QuerySetView):

    def __init__(self):
        super().__init__()
        self.queryset = ESCOSkill.nodes

    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return self.queryset.none()

        qs = self.queryset

        if self.q:
            qs = qs.filter(Q(label__icontains=self.q) | Q(code__icontains=self.q))

        return qs

    def get_result_value(self, result):
        """Return the value of a result."""
        return str(result.concept_url)

    def get_result_label(self, result):
        return result.full_label

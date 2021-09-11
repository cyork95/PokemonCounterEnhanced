from django import forms

from .models import Counter


class RawCounterForm(forms.Form):
    user = forms.CharField(label="Username of Hunter", widget=forms.HiddenInput(), required=False)
    pokemon_id = forms.CharField(label="Pokemon ID (optional)", widget=forms.HiddenInput(), required=False)
    pokemon_name = forms.CharField(label="Pokemon Name",
                                   widget=forms.Select(choices=Counter.POKEMON_NAMES))
    pokemon_game = forms.CharField(label="Pokemon Game",
                                   widget=forms.Select(choices=Counter.POKEMON_GAME_CHOICES))
    count = forms.DecimalField(label="Count", max_digits=10000, decimal_places=0)
    chance = forms.CharField(label="Current Odds", required=False)
    hunting_method = forms.CharField(label="Hunting Method",
                                     widget=forms.Select(choices=Counter.HUNTING_METHOD_CHOICES))
    binomial_distribution = forms.FloatField()
    shiny_charm = forms.BooleanField(label="Shiny Charm?", required=False)
    caught = forms.BooleanField(label="Caught?", required=False)


class ChooseCounterForm(forms.Form):
    user = forms.CharField(label="Username of Hunter", widget=forms.HiddenInput(), required=False)
    count = forms.IntegerField(label="Count", widget=forms.HiddenInput(), required=False)
    pokemon_id = forms.CharField(label="Pokemon ID (optional)", widget=forms.HiddenInput(), required=False)
    pokemon_name = forms.CharField(label="Pokemon Name",
                                   widget=forms.Select(choices=Counter.POKEMON_NAMES))
    pokemon_game = forms.CharField(label="Pokemon Game",
                                   widget=forms.Select(choices=Counter.POKEMON_GAME_CHOICES))
    hunting_method = forms.CharField(label="Hunting Method",
                                     widget=forms.Select(choices=Counter.HUNTING_METHOD_CHOICES))
    shiny_charm = forms.BooleanField(label="Shiny Charm?", required=False)



class CountCounterForm(forms.Form):
    user = forms.CharField(label="Username of Hunter", widget=forms.HiddenInput(), required=False)
    pokemon_id = forms.CharField(label="Pokemon ID (optional)", widget=forms.HiddenInput(), required=False)
    pokemon_name = forms.CharField(label="Pokemon Name",
                                   widget=forms.HiddenInput(), required=False)
    pokemon_game = forms.CharField(label="Pokemon Game",
                                   widget=forms.HiddenInput(), required=False)
    count = forms.DecimalField(label="Count", max_digits=10000, decimal_places=0, widget=forms.HiddenInput(),
                               required=False)
    chance = forms.CharField(label="Current Odds", widget=forms.HiddenInput(), required=False)
    chance_string = forms.CharField(label="Current Odds", widget=forms.HiddenInput(), required=False)
    hunting_method = forms.CharField(label="Hunting Method",
                                     widget=forms.HiddenInput(), required=False)
    binomial_distribution = forms.FloatField(widget=forms.HiddenInput(), required=False)
    shiny_charm = forms.BooleanField(label="Shiny Charm?", widget=forms.HiddenInput(), required=False)
    caught = forms.BooleanField(label="Caught?", widget=forms.HiddenInput(), required=False)

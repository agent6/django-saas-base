from django import forms

CHECKBOX_CLASS = "h-4 w-4 rounded border-slate-300 text-slate-700 focus:ring-slate-500"
INPUT_CLASS = (
    "w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm "
    "focus:border-slate-500 focus:outline-none focus:ring-1 focus:ring-slate-500"
)


def apply_tailwind_classes(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
            widget.attrs.setdefault("class", CHECKBOX_CLASS)
            continue
        if isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs.setdefault("class", INPUT_CLASS)
            continue
        widget.attrs.setdefault("class", INPUT_CLASS)

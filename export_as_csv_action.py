#-*-coding:utf-8-*-
"""
http://djangosnippets.org/snippets/2020/
"""
import csv
from django.http import HttpResponse

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    http://djangosnippets.org/snippets/2020/

    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset
        field_names=list(field_names)
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)).encode('utf-8') for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv



# example usage:
#
#class SubscriberAdmin(admin.ModelAdmin):
#    raw_id_fields = ('logged_in_as',)
#    list_display = ('email', 'date', 'logged_in_as',)
#    actions = [export_as_csv_action("Export selected emails as CSV file", fields=['email'], header=False),]
#
#admin.site.register(UpdatesSubscriber, SubscriberAdmin)
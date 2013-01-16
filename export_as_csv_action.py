"""
http://djangosnippets.org/snippets/2712/
"""
import csv
from django.http import HttpResponse


def export_select_fields_csv_action(description="Export selected objects as CSV file",
                                    fields=None, exclude=None, header=True):
    """
    This function returns an export csv action

    'fields' is a list of tuples denoting the field and label to be exported. Labels
    make up the header row of the exported file if header=True.

        fields=[
                ('field1', 'label1'),
                ('field2', 'label2'),
                ('field3', 'label3'),
            ]

    'exclude' is a flat list of fields to exclude. If 'exclude' is passed,
    'fields' will not be used. Either use 'fields' or 'exclude.'

        exclude=['field1', 'field2', field3]

    'header' is whether or not to output the column names as the first row

    Based on: http://djangosnippets.org/snippets/2020/
    """

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = [field.name for field in opts.fields]
        labels = []
        if exclude:
            field_names = [v for v in field_names if v not in exclude]
        elif fields:
            field_names = fields
        #            field_names = [k for k, v in fields if k in field_names]
        #            labels = [v for k, v in fields if k in field_names]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            if labels:
                writer.writerow(labels)
            else:
                writer.writerow(field_names)
        for obj in queryset:
            row = []
            for field in field_names:
                if hasattr(obj, field):
                    row.append(unicode(getattr(obj, field)).encode('utf-8'))
                elif hasattr(modeladmin, field):
                    row.append(unicode(getattr(modeladmin, field)(obj)).encode('utf-8'))
                else:
                    raise Exception('No such field')
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv


    ## Usage
    #
    #class ExampleModelAdmin(admin.ModelAdmin):
    #    raw_id_fields = ('field1',)
    #    list_display = ('field1', 'field2', 'field3',)
    #    actions = [
    #        export_as_csv_action("Export Sepecial Report",
    #            fields=[
    #                ('field1', 'label1'),
    #                ('field2', 'label2'),
    #                ('field3', 'label3'),
    #                ],
    #            header=True
    #        ),
    #        ]
    #
    #admin.site.register(ExampleMode, ExampleModelAdmin)
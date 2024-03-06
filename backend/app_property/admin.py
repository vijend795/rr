from django.contrib import admin
from app_property.models import Property ,SubProperty,SubPropertyType
# Register your models here.
class SubPropertyInline(admin.StackedInline):
    model=SubProperty
    extra=1





# admin

class PropertyAdmin(admin.ModelAdmin):
    model=Property
    list_display=('custom_id',)
    inlines=[SubPropertyInline]
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
                                            'unit',
                                            'plot',
                                            'floor',
                                            'building',
                                            'tower',
                                            ) \
                           .prefetch_related(
                               'sub_properties',
                               'unit__unit_floor_relationships__floor',
                                'unit__unit_floor_relationships__floor__floor_tower_relationships',
                                'unit__unit_floor_relationships__floor__floor_plot_relationships__plot',
                                'unit__unit_floor_relationships__floor__floor_plot_relationships__plot__plot_building_relationships__building',
                                'unit__unit_floor_relationships__floor__floor_plot_relationships__plot__plot_building_relationships__building__area',
                                'unit__unit_floor_relationships__floor__floor_plot_relationships__plot__plot_building_relationships__building__area__area_locality_relations__locality',
                                'unit__unit_floor_relationships__floor__floor_plot_relationships__plot__plot_building_relationships__building__area__area_locality_relations__locality__city__state',
                                'unit__unit_floor_relationships__floor__floor_tower_relationships__tower',
                                'unit__unit_floor_relationships__floor__floor_tower_relationships__tower__tower_building_relationships__building',
                                
                                'floor__floor_plot_relationships__plot__plot_building_relationships__building__area__area_locality_relations__locality__city__state',
                                'floor__floor_tower_relationships__tower__tower_building_relationships__building__area__area_locality_relations__locality__city__state',
                                'tower__tower_building_relationships__building__area__area_locality_relations__locality__city__state',
                                'building__area__area_locality_relations__locality__city__state',
                                'building__plot_building_relationships__plot__area__area_locality_relations__locality__city__state',
                                'plot__area__area_locality_relations__locality__city__state'
                                
                                )
        return queryset

class SubPropertyAdmin(admin.ModelAdmin):
    model=SubProperty
    list_display=('custom_id',)
 
class SubPropertyTypeAdmin(admin.ModelAdmin):
    model=SubPropertyType
    list_display=('custom_id',)
 


admin.site.register(Property,PropertyAdmin)
admin.site.register(SubProperty,SubPropertyAdmin)
admin.site.register(SubPropertyType,SubPropertyTypeAdmin)
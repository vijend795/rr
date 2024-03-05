from django.shortcuts import render
import csv
from app_data_import.forms import PropertyDataImportForm
from app_address.models import Country,City,State,Locality,LocalityType,Block,Plot, Landmark, Street,Building, Tower, Floor, Unit, FloorPlotRelationship, FloorTowerRelationship, UnitFloorRelationship, PlotBuildingRelationship, StreetBuildingRelationship,StreetPlotRelationship, TowerBuildingRelationship,LandmarkBuildingRelationship, LandmarkPlotRelationship
from django.views.generic import TemplateView
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from app_address.models import Area
from django.db.models import Q,Count

def Upload_property_data(request):
    form=PropertyDataImportForm()
    
    if request.method=='POST':
        
        form =PropertyDataImportForm(request.POST,request.FILES)
        if form.is_valid():
            csv_file=request.FILES['csv_file']
            try:
                print(csv_file)
                # print("temporary path :",csv_file.temporary_file_path())
                with open(csv_file.temporary_file_path(), 'r', encoding='utf-8', errors='ignore') as f:
                # with csv_file.open(mode='r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    # print header data for header_mapping 
                    # for h in header:
                    #     print(f" '{h}':'{h.lower()}', ")
                    header_mapping={
                            'Created_By':'created_by', 
                            'Created_Date':'created_date', 
                            'Serial_No':'serial_no', 
                            'Property_ID':'property_id', 
                            'Last_Updated_By':'last_updated_by', 
                            'Last_Updated_On':'last_updated_on', 
                            'Hot':'hot', 
                            'Shared_Website':'shared_website', 
                            'MCG_Property_Code':'mcg_property_code', 
                            'File_Name':'file_name', 
                            'Follow_Up_Status':'follow_up_status', 
                            'Next_Follow_Up':'next_follow_up', 
                            'Follow_Up_History':'follow_up_history', 
                            'Land_Use':'land_use', 
                            'Construction_Completion_Date':'construction_completion_date', 
                            'Project_Structure':'project_structure', 
                            'Project_ID':'project_id', 
                            'Project_Name':'project_name', 
                            'Possession_Status':'possession_status', 
                            'Plot_Area_Min':'plot_area_min', 
                            'Plot_Area_Max':'plot_area_max', 
                            'Unit_Plot_Area':'unit_plot_area', 
                            'Plot_No':'plot_no', 
                            'Total_Floor':'total_floor', 
                            'Total_BuildUp_Area':'total_buildup_area', 
                            'Property_Status':'property_status', 
                            'Property_Status_Follow_Up':'property_status_follow_up', 
                            'Property_Status_Modified':'property_status_modified', 
                            'Property_Status_History':'property_status_history', 
                            'Property_For':'property_for', 
                            'Calling_Update':'calling_update', 
                            'Property_Type':'property_type', 
                            'Property_Sub_Type':'property_sub_type', 
                            'Property_Use':'property_use', 
                            'Full_Address':'full_address', 
                            'Building_Name':'building_name', 
                            'Wing':'wing', 
                            'Unit_No':'unit_no', 
                            'Floor':'floor', 
                            'Block':'block', 
                            'Landmark':'landmark', 
                            'All_Locality':'all_locality', 
                            'Road':'road', 
                            'Colony':'colony', 
                            'Locality_1':'locality_1', 
                            'Locality_2':'locality_2', 
                            'Sector':'sector', 
                            'Area':'area', 
                            'City':'city', 
                            'State':'state', 
                            'Country':'country', 
                            'Pin_Code':'pin_code', 
                            'Keys_With':'keys_with', 
                            'Owner_ID':'owner_id', 
                            'Owner_Full_Name':'owner_full_name', 
                            'Owner_All_Contact':'owner_all_contact', 
                            'Owner_Source_Type':'owner_source_type', 
                            'Owner_Company_Name':'owner_company_name', 
                            'Owner_Name':'owner_name', 
                            'Owner_Mobile_1':'owner_mobile_1', 
                            'Owner_Mobile_2':'owner_mobile_2', 
                            'Owner_Office_Landline':'owner_office_landline', 
                            'Owner_Home_Landline':'owner_home_landline', 
                            'Owner_Email_1':'owner_email_1', 
                            'Owner_Email_2':'owner_email_2', 
                            'Owner_Address':'owner_address', 
                            'Owner_Caretaker_Name':'owner_caretaker_name', 
                            'Owner_Caretaker_No_1':'owner_caretaker_no_1', 
                            'Owner_Caretaker_No_2':'owner_caretaker_no_2', 
                            'Co_Owner_Name':'co_owner_name', 
                            'Co_Owner_No_1':'co_owner_no_1', 
                            'Co_Owner_No_2':'co_owner_no_2', 
                            'Owner_Comment':'owner_comment', 
                            'Super_Area_Min':'super_area_min', 
                            'Super_Area_Max':'super_area_max', 
                            'Unit_Area':'unit_area', 
                            'Maintenance_Charge_PSF':'maintenance_charge_psf', 
                            'Maintenance_Charge_Min_Rs':'maintenance_charge_min_rs', 
                            'Maintenance_Charge_Max_Rs':'maintenance_charge_max_rs', 
                            'Efficiency':'efficiency', 
                            'Covered_Area_Min':'covered_area_min', 
                            'Covered_Area_Max':'covered_area_max', 
                            'Expected_Rent_PSF':'expected_rent_psf', 
                            'Expected_Rent_Min_Rs':'expected_rent_min_rs', 
                            'Expected_Rent_Max_Rs':'expected_rent_max_rs', 
                            'For_Sale':'for_sale', 
                            'Sale_Price_PSF':'sale_price_psf', 
                            'Sale_Price_Min_Rs':'sale_price_min_rs', 
                            'Sale_Price_Max_Rs':'sale_price_max_rs', 
                            'Sale_Cash_Ratio':'sale_cash_ratio', 
                            'Amenities':'amenities', 
                            'Vastu':'vastu', 
                            'Furnishing_Type':'furnishing_type', 
                            'Furnishing_Quality':'furnishing_quality', 
                            'Property_Available':'property_available', 
                            'Property_Remarks_Internal':'property_remarks_internal', 
                            'Property_Remarks_External':'property_remarks_external', 
                            'Furnishing_Detail':'furnishing_detail', 
                            'Property_Condition':'property_condition', 
                            'Cabin_No':'cabin_no', 
                            'Workstation_No':'workstation_no', 
                            'Car_Parking_No':'car_parking_no', 
                            'Conference_No':'conference_no', 
                            'Pantry':'pantry', 
                            'Server_Room':'server_room', 
                            'Meeting_Room':'meeting_room', 
                            'Cubical':'cubical', 
                            'Air_Condition':'air_condition', 
                            'Internal_Comments':'internal_comments', 
                            'External_Comments':'external_comments', 
                            'Assigned_Manger':'assigned_manger', 
                            'Group':'group', 
                            'Teams':'teams', 
                            'Source_Channel':'source_channel', 
                            'Sub_Source_Channel':'sub_source_channel', 
                            'Pre_Rented':'pre_rented', 
                            'Company_Name':'company_name', 
                            'Pre_Rented_Super_Area_Min':'pre_rented_super_area_min', 
                            'Pre_Rented_Super_Area_Max':'pre_rented_super_area_max', 
                            'ROI':'roi', 
                            'Sale_Price_Pre_Rented_PSF':'sale_price_pre_rented_psf', 
                            'Sale_Price_Pre_Rented_Min_Rs':'sale_price_pre_rented_min_rs', 
                            'Sale_Price_Pre_Rented_Max_Rs':'sale_price_pre_rented_max_rs', 
                            'Pre_Rented_Cash_Ratio':'pre_rented_cash_ratio', 
                            'Sale_Remark':'sale_remark', 
                            'Pre_Rented_Plot_Area_Min':'pre_rented_plot_area_min', 
                            'Pre_Rented_Plot_Area_Max':'pre_rented_plot_area_max', 
                            'Pre_Rented_Unit_Area':'pre_rented_unit_area', 
                            'Pre_Rented_Covered_Area_Min':'pre_rented_covered_area_min', 
                            'Pre_Rented_Covered_Area_Max':'pre_rented_covered_area_max', 
                            'Pre_Rented_Maintenance_PSF':'pre_rented_maintenance_psf', 
                            'Pre_Rented_Maintenance_Min':'pre_rented_maintenance_min', 
                            'Pre_Rented_Maintenance_Max':'pre_rented_maintenance_max', 
                            'Lease_Start':'lease_start', 
                            'Possession_Date':'possession_date', 
                            'Lease_Period':'lease_period', 
                            'Security_Deposit':'security_deposit', 
                            'Lock_in_Period':'lock_in_period', 
                            'Monthly_Rent_Min_Rs':'monthly_rent_min_rs', 
                            'Monthly_Rent_Max_Rs':'monthly_rent_max_rs', 
                            'Rent_Escalation':'rent_escalation', 
                            'Pre_Rented_Remark':'pre_rented_remark', 
                            'Extra1':'extra1', 
                            'Attachment':'attachment', 
                            'Video_Link':'video_link', 
                    
                    }
                    
                    data={variable_name:None for header_name,variable_name in header_mapping.items()}
                    
                    
                    i=0
                  
                    country_created_count=0
                    country_updated_count=0
                    
                    state_created_count=0
                    state_updated_count=0
                    
                    city_created_count=0
                    city_updated_count=0
                    
                    locality_created_count=0
                    locality_updated_count=0
                    
                    not_found=0
                    found_one=0
                    found_many=0
                    print("Data upload from data sheet process initialized .......")
                    for row in reader:
                        if header is not None:
                            for header_name, variable_name in header_mapping.items():
                                index=header.index(header_name) if header_name in header else -1
                                if index >=0:
                                    data[variable_name]=row[index]
                        
                        # country_created_count, country_updated_count = update_or_create_country(data=data, country_created_count=country_created_count, country_updated_count=country_updated_count)
                        # state_created_count, state_updated_count = update_or_create_state(data=data, state_created_count=state_created_count, state_updated_count=state_updated_count)
                        # city_created_count, city_updated_count = update_or_create_city(data=data, city_created_count=city_created_count, city_updated_count=city_updated_count)
                        # update_or_create_locality(data=data)
                        
                        # not_found,found_one,found_many=check_area(data=data,not_found=not_found,found_one=found_one,found_many=found_many)
                       
                        # update_or_create_block(data=data)
                        
                        area_object=update_or_create_area(data=data)
                        
                        # for creating Plot, Building, block etc
                        update_or_create_other_plot_object(data=data, area_obj=area_object)
                        
                        
                        # if i==0:
                        #     print(data)
                        #     i+=1
                    print(f"Country data updated from data sheet by import method \nCountry Created:{country_created_count},\nCountry Updated:{country_updated_count}")
                    print(f"State data updated from data sheet by import method \nState Created:{state_created_count},\nstate Updated:{state_updated_count}")
                    print(f"City data updated from data sheet by import method \ncity Created:{city_created_count},\ncity Updated:{city_updated_count}")
                    print(f"Area check update :\n Not found:{not_found},\n Found One :{found_one},\n Found Many :{found_many}")
                    print("Data upload from data sheet process ended!")
                    return render(request, 'success_url/success_import_property_data.html')
            except Exception as e:
                # Handle exceptions (e.g., file format errors, database errors)
                return render(request, 'error_404/import_error.html', {'error_message': str(e)})
            
            

            return render (request,'success_import_property_data.html')
        else:
            form=PropertyDataImportForm()
        
    
        
    return render(request,'import_data/upload_property_data.html',{'form': form})


class UploadStatus(TemplateView):
    template_name='success_url/success_import_property_data.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context data here if needed
        return context


def update_or_create_country(data,country_created_count,country_updated_count):
    country =data['country']
    if country:
        try:
            country_data=Country.objects.get(name=data['country'])
            country_updated_count+=1
        except Country.DoesNotExist:
            Country.objects.create(name=data['country'])
            country_created_count+=1
    else:
       
        print("Country data is not available in data sheet, property ID:",data['property_id'])
    return country_created_count, country_updated_count

def update_or_create_state(data,state_created_count,state_updated_count):
    state =data['state']
    if state:
        try:
            state_data=State.objects.get(name=state)
            state_updated_count+=1
        except State.DoesNotExist:
            State.objects.create(name=state,country=Country.objects.get(name=data['country']))
            state_created_count+=1
    else:
       
        print("state data is not available in data sheet, property ID:",data['property_id'])
    return state_created_count, state_updated_count

def update_or_create_city(data,city_created_count,city_updated_count):
    city =data['city']
    if city:
        try:
            city_data=City.objects.get(name=city)
            city_updated_count+=1
        except City.DoesNotExist:
            City.objects.create(name=city,state=State.objects.get(name=data['state']))
            city_created_count+=1
    else:
       
        print("city data is not available in data sheet, property ID:",data['property_id'])
    return city_created_count, city_updated_count

def update_or_create_locality(data):
    city_name = data['city']
    state_name = data['state']

    if not city_name or not state_name:
        print("Error: Creating locality failed. City and state information is not available.")
        return

    try:
        city = City.objects.get(name=city_name, state__name=state_name)
    except City.DoesNotExist:
        city, created = City.objects.get_or_create(name=city_name, state=State.objects.get(name=state_name))
        print(f"Error: City '{city_name}' in state '{state_name}' does not exist.")
        return

    for field_name in ['sector', 'colony', 'area', 'locality_1', 'locality_2']:
        locality_name = data.get(field_name)
        if locality_name:
            # Determine locality type based on the field name or locality name
            if field_name.capitalize() in ['Sector', 'Colony']:
                locality_type = field_name.capitalize()
            elif 'Vihar' in locality_name.capitalize():
                locality_type = 'Vihar'
            elif 'Village' in locality_name.capitalize():
                locality_type = 'Village'
            else:
                locality_type = 'Area'
                
            try:
                # Get or create the LocalityType object
                locality_type_obj, _ = LocalityType.objects.get_or_create(name=locality_type)
                
                # Create or update the Locality object
                locality, created = Locality.objects.get_or_create(name=locality_name, city=city)
                locality.locality_type=locality_type_obj
                locality.save()
            except Exception as e:
                print(f"Error: {e}")

    print("Locality update or creation completed.")



def update_or_create_block(data):
    block=data['block']
    sector = data['sector']
    colony = data['colony']
    area = data['area']
    locality_1 = data['locality_1']
    locality_2 = data['locality_2']
    pin_code = data['pin_code']
    city_name = data['city']
    state_name = data['state']
    
    locality_set=set()
    if block:
        if city_name and state_name:
            if sector:
                try:
                    locality_obj = Locality.objects.get(name=sector, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    locality_set.add(locality_obj)
                except locality_obj.DoesNotExist:
                    print(f"Locality not exits by sector :{sector} ")
            if colony:
                try:
                    locality_obj = Locality.objects.get(name=colony, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    locality_set.add(locality_obj)
                except locality_obj.DoesNotExist:
                    print(f"Locality not exits by colony :{colony} ")
                    
            if area:
                try:
                    locality_obj = Locality.objects.get(name=area, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    locality_set.add(locality_obj)
                except locality_obj.DoesNotExist:
                    print(f"Locality not exits by area :{area} ")
            if locality_1:
                try:
                    locality_obj = Locality.objects.get(name=locality_1, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    locality_set.add(locality_obj)
                except locality_obj.DoesNotExist:
                    print(f"Locality not exits by Locality 1 :{locality_1} ")
            if locality_2:
                try:
                    locality_obj = Locality.objects.get(name=locality_2, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    locality_set.add(locality_obj)
                except locality_obj.DoesNotExist:
                    print(f"Locality not exits by locality 2 :{locality_2} ")
                    
        if locality_set:
            all_localities_name=set(locality.name for locality in locality_set)
            if colony and colony != 'South Delhi':
                locality_name=colony
                try:
                    search_block = Block.objects.get(name=block, locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))))
                except Block.DoesNotExist:
                    block, created = Block.objects.get_or_create(name=block,
                                                                 locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))),
                                                                 remark=all_localities_name
                                                                 )
            elif locality_1 and locality_1 != "South Delhi":
                locality_name=locality_1
                try:
                    search_block=Block.objects.get(name=block, locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))))
                except Block.DoesNotExist:
                    block, created = Block.objects.get_or_create(name=block,
                                                                 locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))),
                                                                 remark=all_localities_name
                                                                 )
            elif area and area != "Udyog Vihar" and area != 'South Delhi' and area != 'Lajpat Nagar' and area != 'Devilal Colony':
                locality_name=area
                try:
                    search_block=Block.objects.get(name=block, locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))))
                except Block.DoesNotExist:
                    block, created = Block.objects.get_or_create(name=block,
                                                                 locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))),
                                                                 remark=all_localities_name
                                                                 )
            elif locality_2 :
                locality_name=locality_2
                try:
                    search_block=Block.objects.get(name=block, locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))))
                except Block.DoesNotExist:
                    block, created = Block.objects.get_or_create(name=block,
                                                                 locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))),
                                                                 remark=all_localities_name
                                                                 )
            elif sector :
                locality_name=sector
                try:
                    search_block=Block.objects.get(name=block, locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))))
                except Block.DoesNotExist:
                    block, created = Block.objects.get_or_create(name=block,
                                                                 locality=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name))),
                                                                 remark=all_localities_name
                                                                 )
            else:
                print("Block has no locality to match with data row id ",data['property_id'])
                
      
            


# def check_area(data,not_found,found_one,found_many):
def update_or_create_area(data):
    block=data['block']
    sector = data['sector']
    colony = data['colony']
    area = data['area']
    locality_1 = data['locality_1']
    locality_2 = data['locality_2']
    pin_code = data['pin_code']
    city_name = data['city']
    state_name = data['state']
    locality_set=set()
    area_object=None
    if  city_name and state_name:
        if sector:
            try:
                locality_obj = Locality.objects.get(name=sector, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by sector :{sector} ")
        if colony:
            try:
                locality_obj = Locality.objects.get(name=colony, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by colony :{colony} ")
                
        if area:
            try:
                locality_obj = Locality.objects.get(name=area, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by area :{area} ")
        if locality_1:
            try:
                locality_obj = Locality.objects.get(name=locality_1, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by Locality 1 :{locality_1} ")
        if locality_2:
            try:
                locality_obj = Locality.objects.get(name=locality_2, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by locality 2 :{locality_2} ")
        
                
                
                
    locality_set=set()
    if city_name and state_name:
        if sector:
            try:
                locality_obj = Locality.objects.get(name=sector, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by sector :{sector} ")
        if colony:
            try:
                locality_obj = Locality.objects.get(name=colony, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by colony :{colony} ")
                
        if area:
            try:
                locality_obj = Locality.objects.get(name=area, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by area :{area} ")
        if locality_1:
            try:
                locality_obj = Locality.objects.get(name=locality_1, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by Locality 1 :{locality_1} ")
        if locality_2:
            try:
                locality_obj = Locality.objects.get(name=locality_2, city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                locality_set.add(locality_obj)
            except locality_obj.DoesNotExist:
                print(f"Locality not exits by locality 2 :{locality_2} ")
                
    if locality_set:
      
        locality_ids = [locality.id for locality in locality_set]
        search_area=Area.objects.all()
        
        # search_area = search_area.filter(localities__in=locality_ids)
        
        search_area=search_area.annotate(num_localities=Count('localities')).filter(num_localities=len(locality_ids))
        
        final_search_result = []

        if search_area:
            for area in search_area:
                search_locality_ids = set(locality.id for locality in area.localities.all())
                if set(locality_ids) == search_locality_ids:
                    final_search_result.append(area)
                
        # find block object
        block_obj=None 
    
        if block and city_name and state_name:  # Check if block, city_name, and state_name are provided
            locality_name=None
            block=data['block']
            sector_name = data['sector']
            colony_name = data['colony']
            area_name = data['area']
            locality_1_name = data['locality_1']
            locality_2_name = data['locality_2']
            pin_code = data['pin_code']
            city_name = data['city']
            state_name = data['state']
            # Determine the locality_name based on the conditions
            if colony_name and colony_name != 'South Delhi':
                locality_name = colony_name
            elif locality_1_name and locality_1_name != "South Delhi":
                locality_name = locality_1_name
            elif area_name and area_name not in ["Udyog Vihar", 'South Delhi', 'Lajpat Nagar', 'Devilal Colony']:
                locality_name = area_name
            elif locality_2_name:
                locality_name = locality_2_name
            elif sector_name:
                locality_name = sector_name

            # Retrieve the block object
            print("locality Name :",locality_name)
            if locality_name:  # Ensure that locality_name is not None
                try:
                    # Query for the block object using locality_name, city_name, and state_name
                    try:
                        locality_obj=Locality.objects.get(name=locality_name,city=City.objects.get(name=city_name,state=State.objects.get(name=state_name)))
                    except locality_obj.DoesNotExist:
                        print("Locality not exits for block obj :",locality_name)
                    # if locality Obj exits then find block obj
                    block_obj = Block.objects.get(name=block, locality=locality_obj )
                except Block.DoesNotExist:
                    print(f"Block matching query does not exist for block: {block}, locality: {locality_name}, city: {city_name}, state: {state_name}")

      
        if len(final_search_result)==0:
            area_obj = Area.objects.create(pin_code=pin_code)
            area_obj.localities.add(*locality_set)
            if block_obj is not None:
                area_obj.block=block_obj
            print("Area created:", area_obj)
            area_object=area_obj
            # print("error cant found area for locality :",locality_set)
            
        
            
        if final_search_result:
            if len(final_search_result)==1:
                for area in final_search_result:
                    if block_obj is not None:
                        area.block=block_obj
                        area.save()
                        print("Block updated in area object")
                        area_object=area
                # print("Area matched , write update code below if you want to update ")
                
            if len(final_search_result)>1:
                multiple_search_area_locality_ids_group=set()
                for area in final_search_result:
                    locality_ids=tuple(locality.id for locality in area.localities.all())
                    multiple_search_area_locality_ids_group.add(locality_ids)
                
                print("Error more then 2 area found for locality:",locality_ids)
                print("Search area :",multiple_search_area_locality_ids_group)
                
    return area_object          
                
    
    
   
def update_or_create_other_plot_object(data, area_obj):
    plot_no = data['plot_no']
    building = data['building_name']
    tower = data['wing']
    unit_no = data['unit_no']
    floor = data['floor']
    landmark = data['landmark']
    street = data['road']
    
    plot_obj = None
    building_obj = None
    landmark_obj = None
    street_obj = None
    floor_obj = None
    tower_obj = None
    unit_obj=None

    if area_obj and plot_no:
        plot_obj, created = Plot.objects.get_or_create(plot_no=plot_no, area=area_obj)
        if created:
            print(f"Plot object created with plot_no: {plot_no} and area: {area_obj}")
        else:
            print(f"Plot object already exists with plot_no: {plot_no} and area: {area_obj}")

    if area_obj and building:
        building_obj, created = Building.objects.get_or_create(name=building, area=area_obj)
        if created:
            print(f"Building object created with name: {building} and area: {area_obj}")
        else:
            print(f"Building object already exists with name: {building} and area: {area_obj}")

    if area_obj and landmark:
        landmark_obj, created = Landmark.objects.get_or_create(name=landmark, area=area_obj)
        if created:
            print(f"Landmark object created with name: {landmark} and area: {area_obj}")
        else:
            print(f"Landmark object already exists with name: {landmark} and area: {area_obj}")

    if area_obj and street:
        street_obj, created = Street.objects.get_or_create(name=street, area=area_obj)
        if created:
            print(f"Street object created with name: {street} and area: {area_obj}")
        else:
            print(f"Street object already exists with name: {street} and area: {area_obj}")

    if floor:
        floor_obj, created = Floor.objects.get_or_create(name=floor)
        if created:
            print(f"Floor object created with name: {floor}")
        else:
            print(f"Floor object already exists with name: {floor}")

    if tower:
        tower_obj, created = Tower.objects.get_or_create(name=tower)
        if created:
            print(f"Tower object created with name: {tower}")
        else:
            print(f"Tower object already exists with name: {tower}")
            
    if unit_no:
        unit_obj, created = Unit.objects.get_or_create(name=unit_no)
        if created:
            print(f"Unit object created with name: {unit_no}")
        else:
            print(f"Unit object already exists with name: {unit_no}")

    if floor_obj and plot_obj:
        floor_plot_relationship_obj, created = FloorPlotRelationship.objects.get_or_create(
            floor=floor_obj,
            plot=plot_obj
        )
        if created:
            print(f"FloorPlotRelationship object created for floor: {floor_obj} and plot: {plot_obj}")
        else:
            print(f"FloorPlotRelationship object already exists for floor: {floor_obj} and plot: {plot_obj}")
    
    if floor_obj and tower_obj:
        print(f"floor {floor_obj} and tower {tower_obj}")
        floor_tower_relationship_obj, created = FloorTowerRelationship.objects.get_or_create(
            floor=floor_obj,
            tower=tower_obj
        )
        if created:
            print(f"FloorTowerRelationship object created for floor: {floor_obj} and tower: {tower_obj}")
        else:
            print(f"FloorTowerRelationship object already exists for floor: {floor_obj} and tower: {tower_obj}")
    
    if plot_obj and building_obj:
        plot_building_relationship_obj, created = PlotBuildingRelationship.objects.get_or_create(
            plot=plot_obj,
            building=building_obj
        )
        if created:
            print(f"PlotBuildingRelationship object created for plot: {plot_obj} and building: {building_obj}")
        else:
            print(f"PlotBuildingRelationship object already exists for plot: {plot_obj} and building: {building_obj}")
    
    if tower_obj and building_obj:
        tower_building_relationship_obj, created = TowerBuildingRelationship.objects.get_or_create(
            tower=tower_obj,
            building=building_obj
        )
        if created:
            print(f"TowerBuildingRelationship object created for tower: {tower_obj} and building: {building_obj}")
        else:
            print(f"TowerBuildingRelationship object already exists for tower: {tower_obj} and building: {building_obj}")
    
    if landmark_obj and building_obj:
        landmark_building_relationship_obj, created = LandmarkBuildingRelationship.objects.get_or_create(
            landmark=landmark_obj,
            building=building_obj
        )
        if created:
            print(f"LandmarkBuildingRelationship object created for landmark: {landmark_obj} and building: {building_obj}")
        else:
            print(f"LandmarkBuildingRelationship object already exists for landmark: {landmark_obj} and building: {building_obj}")
    
    if landmark_obj and plot_obj:
        landmark_plot_relationship_obj, created = LandmarkPlotRelationship.objects.get_or_create(
            landmark=landmark_obj,
            plot=plot_obj
        )
        if created:
            print(f"LandmarkPlotRelationship object created for landmark: {landmark_obj} and plot: {plot_obj}")
        else:
            print(f"LandmarkPlotRelationship object already exists for landmark: {landmark_obj} and plot: {plot_obj}")
    
    if street_obj and plot_obj:
        street_plot_relationship_obj, created = StreetPlotRelationship.objects.get_or_create(
            street=street_obj,
            plot=plot_obj
        )
        if created:
            print(f"StreetPlotRelationship object created for street: {street_obj} and plot: {plot_obj}")
        else:
            print(f"StreetPlotRelationship object already exists for street: {street_obj} and plot: {plot_obj}")
    
    if street_obj and building_obj:
        street_plot_relationship_obj, created = StreetBuildingRelationship.objects.get_or_create(
            street=street_obj,
            building=building_obj
        )
        if created:
            print(f"StreetBuildingRelationship object created for street: {street_obj} and building: {building_obj}")
        else:
            print(f"StreetBuildingRelationship object already exists for street: {street_obj} and building: {building_obj}")

    print(f"floor :{floor}, unit:{unit_no} and floor obj: {floor_obj} , unit object : {unit_obj}")
    if floor_obj and unit_obj:
        
        unit_floor_relationship_obj, created = UnitFloorRelationship.objects.get_or_create(
            floor=floor_obj,
            unit=unit_obj
        )
        if created:
            print(f"UnitFloorRelationship object created for floor: {floor_obj} and unit: {unit_obj}")
        else:
            print(f"UnitFloorRelationship object already exists for floor: {floor_obj} and unit: {unit_obj}")
  
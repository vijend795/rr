from django.shortcuts import render
import csv
from app_data_import.forms import PropertyDataImportForm
from app_address.models import Address,Country,City,State
from django.views.generic import TemplateView
# Create your views here.


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
                    for row in reader:
                        if header is not None:
                            for header_name, variable_name in header_mapping.items():
                                index=header.index(header_name) if header_name in header else -1
                                if index >=0:
                                    data[variable_name]=row[index]
                        
                        update_or_create_country(data=data)
                        
                        # if i==0:
                        #     print(data)
                        #     i+=1
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


def update_or_create_country(data):
    # print("add and update country data from data sheet import initialise.....")
    country =data['country']
    if country:
        try:
            country_data=Country.objects.get(name=data['country'])
            # print('country already exits')
        
        except Country.DoesNotExist:
            Country.objects.create(name=data['country'])
            # print("New Country created :",country)
    else:
        error_count+=1
        print("Country data is not available in data sheet, property ID:",data['property_id'])

    # print(f"add and update country data from data sheet import ended.....\n\n")
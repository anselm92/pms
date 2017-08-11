from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from printing.models import *
from printing_2d.models import *
from printing_3d.models import *


class Command(BaseCommand):
    help = 'Initializes the database'

    def handle(self, *args, **options):
        # Printing
        self.stdout.write('CostCenter')
        cost_center_1 = CostCenter(name='Skripten')
        cost_center_1.save()
        cost_center_2 = CostCenter(name='SET')
        cost_center_2.save()
        cost_center_3 = CostCenter(name='Unity')
        cost_center_3.save()

        self.stdout.write('ExternalCustomer')
        external_customer_1 = ExternalCustomer(first_name='Michael', last_name='Rothstein',
                                               mail_address='MichaelDRothstein@dayrep.com')
        external_customer_1.save()
        external_customer_2 = ExternalCustomer(first_name='Jeannette', last_name='Zahn',
                                               mail_address='JeannetteAZahn@dayrep.com')
        external_customer_2.save()
        external_customer_3 = ExternalCustomer(first_name='Neil', last_name='Smith',
                                               mail_address='NeilMSmith@teleworm.us')
        external_customer_3.save()

        self.stdout.write('User')
        django_user_1 = User.objects.create_superuser(username='admin', first_name='Johnny', last_name='Reed',
                                                      email='JohnnyEReed@teleworm.us', password='admin', is_staff=True)
        django_user_2 = User.objects.create_user(username='test', first_name='Richard', last_name='Bronson',
                                                 email='RichardTBronson@armyspy.com', password='test')

        self.stdout.write('StaffCustomer')
        staff_customer_1 = StaffCustomer(first_name=django_user_1.first_name, last_name=django_user_1.last_name,
                                         mail_address=django_user_1.email, user=django_user_1)
        staff_customer_1.save()
        staff_customer_2 = StaffCustomer(first_name=django_user_2.first_name, last_name=django_user_2.last_name,
                                         mail_address=django_user_2.email, user=django_user_2)
        staff_customer_2.save()

        # Printing 2D
        self.stdout.write('CoverSheetColor')
        cover_sheet_color_1 = CoverSheetColor(name='rot', color_code='FF0000')
        cover_sheet_color_1.save()
        cover_sheet_color_2 = CoverSheetColor(name='grün', color_code='00FF00')
        cover_sheet_color_2.save()
        cover_sheet_color_3 = CoverSheetColor(name='blau', color_code='0000FF')
        cover_sheet_color_3.save()

        self.stdout.write('Material2d')
        material_2d_1 = Material2d(name='A3, weiß', color_code='FFFFFF', cost_per_unit=0.20, paper_weight=10,
                                   paper_format='DIN A3')
        material_2d_1.save()
        material_2d_2 = Material2d(name='A4, weiß', color_code='FFFFFF', cost_per_unit=0.10, paper_weight=6.3,
                                   paper_format='DIN A4')
        material_2d_2.save()
        material_2d_3 = Material2d(name='SRA3, weiß', color_code='FFFFFF', cost_per_unit=0.30, paper_weight=15,
                                   paper_format='SRA3')
        material_2d_3.save()

        self.stdout.write('PostProcessing2d')
        post_processing_1 = PostProcessing2d(name='Tackern')
        post_processing_1.save()
        post_processing_2 = PostProcessing2d(name='Binden')
        post_processing_2.save()
        post_processing_3 = PostProcessing2d(name='Lochen')
        post_processing_3.save()

        self.stdout.write('ScriptOrder')
        script_order_1 = ScriptOrder(title='Analysis', amount=250, customer=staff_customer_1,
                                     cover_sheet_color=cover_sheet_color_1)
        script_order_1.save()
        script_order_2 = ScriptOrder(title='Diskrete Strukturen', amount=500, customer=staff_customer_1,
                                     cover_sheet_color=cover_sheet_color_2)
        script_order_2.save()
        script_order_3 = ScriptOrder(title='Lineare Algebra', amount=320, customer=staff_customer_2,
                                     cover_sheet_color=cover_sheet_color_3)
        script_order_3.save()

        self.stdout.write('CustomOrder2d')
        custom_order_1 = CustomOrder2d(title='Bissle drugge', amount=1, customer=external_customer_1,
                                       sided_printing=SIDED_PRINTING_SIMPLEX, chromatic_printing=False,
                                       cost_center=cost_center_1, material=material_2d_1)
        custom_order_1.save()
        custom_order_1.post_processing.add(post_processing_1)
        custom_order_1.post_processing.add(post_processing_2)

        # Printing 3D
        self.stdout.write('Material3d')
        material_3d_1 = Material3d(name='Proto-Pasta Composite PLA ESD / Conductive Filament',
                                   color_code='000000', cost_per_unit=0.13)
        material_3d_1.save()
        material_3d_2 = Material3d(name='PPLA Filament Orange',
                                   color_code='FF7F50', cost_per_unit=0.13)
        material_3d_2.save()

        self.stdout.write('Order3d')
        order_3d_1 = Order3d(title='Unicorn', amount=3, customer=external_customer_1, material=material_3d_2, width=25,
                             height=25, depth=25)
        order_3d_1.save()
        order_3d_2 = Order3d(title='Hippo', amount=1, customer=external_customer_1, material=material_3d_1, width=15,
                             height=15, depth=15)
        order_3d_2.save()

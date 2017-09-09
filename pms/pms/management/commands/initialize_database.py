from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission

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
        admin_user = User.objects.create_superuser(username='admin', first_name='Johnny', last_name='Reed',
                                                   email='JohnnyEReed@teleworm.us', password='admin', is_staff=True)
        skripten_user = User.objects.create_user(username='skripten', first_name='Skripten', last_name='User',
                                                 email='RichardTBronson@armyspy.com', password='passwd123')
        druck_user = User.objects.create_user(username='druck', first_name='Druck', last_name='User',
                                              email='RichardTBronson@armyspy.com', password='passwd123')
        set_user = User.objects.create_user(username='set', first_name='Set', last_name='User',
                                            email='RichardTBronson@armyspy.com', password='passwd123')

        self.stdout.write('StaffCustomer')
        staff_customer_1 = StaffCustomer(first_name=admin_user.first_name, last_name=admin_user.last_name,
                                         mail_address=admin_user.email, user=admin_user)
        staff_customer_1.save()
        staff_customer_2 = StaffCustomer(first_name=skripten_user.first_name, last_name=skripten_user.last_name,
                                         mail_address=skripten_user.email, user=skripten_user)
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

        # self.stdout.write('ScriptOrder')
        # script_order_1 = ScriptOrder(title='Analysis', amount=250, customer=staff_customer_1,
        #                             cover_sheet_color=cover_sheet_color_1)
        # script_order_1.save()
        # script_order_2 = ScriptOrder(title='Diskrete Strukturen', amount=500, customer=staff_customer_1,
        #                             cover_sheet_color=cover_sheet_color_2)
        # script_order_2.save()
        # script_order_3 = ScriptOrder(title='Lineare Algebra', amount=320, customer=staff_customer_2,
        #                             cover_sheet_color=cover_sheet_color_3)
        # script_order_3.save()

        # self.stdout.write('CustomOrder2d')
        # custom_order_1 = CustomOrder2d(title='Bissle drugge', amount=1, customer=external_customer_1,
        #                               sided_printing=SIDED_PRINTING_SIMPLEX, chromatic_printing=False,
        #                               cost_center=cost_center_1, material=material_2d_1)
        # custom_order_1.save()
        # custom_order_1.post_processing.add(post_processing_1)
        # custom_order_1.post_processing.add(post_processing_2)

        # Printing 3D
        self.stdout.write('Material3d')
        material_3d_1 = Material3d(name='Proto-Pasta Composite PLA ESD / Conductive Filament',
                                   color_code='000000', cost_per_unit=0.13)
        material_3d_1.save()
        material_3d_2 = Material3d(name='PPLA Filament Orange',
                                   color_code='FF7F50', cost_per_unit=0.13)
        material_3d_2.save()

        # self.stdout.write('Order3d')
        # order_3d_1 = Order3d(title='Unicorn', amount=3, customer=external_customer_1, material=material_3d_2, width=25,
        #                     height=25, depth=25)
        # order_3d_1.save()
        # order_3d_2 = Order3d(title='Hippo', amount=1, customer=external_customer_1, material=material_3d_1, width=15,
        #                     height=15, depth=15)
        # order_3d_2.save()

        self.stdout.write('Permissions')
        # TODO: add permissions for all views
        content_type = ContentType.objects.filter(app_label="printing", model="dashboard")
        if not content_type:
            content_type = ContentType.objects.create(app_label="printing", model="dashboard")

        if not Permission.objects.filter(content_type=content_type, codename="dashboard_show"):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename="dashboard_show",
                                      name="Can view %s" % content_type.model)

        # Retrieve and set all static permissions for groups
        dashboard_perm = Permission.objects.get(codename="dashboard_show")
        duplicate_order_perm = Permission.objects.get(codename="add_order")
        change_order = Permission.objects.get(codename="change_order")
        add_staffcomment_perm = Permission.objects.get(codename="add_staffcomment")
        add_customorder_perm = Permission.objects.get(codename="add_customorder2d")
        add_scriptorder_perm = Permission.objects.get(codename="add_scriptorder")

        druck_group = Group(name='druck')
        druck_group.save()
        druck_group.permissions.add(dashboard_perm)
        druck_group.permissions.add(duplicate_order_perm)
        druck_group.permissions.add(change_order)
        druck_group.permissions.add(add_staffcomment_perm)
        druck_group.permissions.add(add_customorder_perm)
        druck_group.permissions.add(add_scriptorder_perm)

        skripten_group = Group(name='skripten')
        skripten_group.save()
        skripten_group.permissions.add(dashboard_perm)
        skripten_group.permissions.add(duplicate_order_perm)
        skripten_group.permissions.add(change_order)
        skripten_group.permissions.add(add_staffcomment_perm)
        skripten_group.permissions.add(add_customorder_perm)
        skripten_group.permissions.add(add_scriptorder_perm)

        set_group = Group(name='set')
        set_group.save()
        set_group.permissions.add(dashboard_perm)
        set_group.permissions.add(duplicate_order_perm)
        set_group.permissions.add(change_order)
        set_group.permissions.add(add_staffcomment_perm)
        set_group.permissions.add(add_customorder_perm)

        skripten_user.groups.add(skripten_group)
        druck_user.groups.add(druck_group)
        set_user.groups.add(set_group)

        # Create and assign all custom filter permissions to groups
        # Necessary filters for druck group
        filter_druck_can_see_customorders = CustomGroupFilter(key='customorder2d__isnull', group=druck_group,
                                                              value_boolean=False,
                                                              object_id=0)
        filter_druck_can_see_scriptorders = CustomGroupFilter(key='scriptorder__isnull', group=druck_group,
                                                              value_boolean=False,
                                                              object_id=0)
        filter_druck_can_see_3dorders = CustomGroupFilter(key='order3d__isnull', group=druck_group,
                                                          value_boolean=False,
                                                          object_id=0)
        filter_druck_can_see_customorders.save()
        filter_druck_can_see_scriptorders.save()
        filter_druck_can_see_3dorders.save()

        # Filters for group skripten
        filter_skripten_can_see_scriptorders = CustomGroupFilter(key='scriptorder__isnull', group=skripten_group,
                                                                 value_boolean=False,
                                                                 object_id=0)
        filter_skripten_can_see_customorders_with_cost_center_scripts = CustomGroupFilter(
            key='customorder2d__cost_center', group=skripten_group,
            content_type=ContentType.objects.get(model='costcenter'),
            object_id=CostCenter.objects.get(name='Skripten').id)
        filter_skripten_can_see_scriptorders.save()
        filter_skripten_can_see_customorders_with_cost_center_scripts.save()

        # Filters for SET
        filter_set_can_see_customorders_with_cost_center_set = CustomGroupFilter(
            key='customorder2d__cost_center', group=set_group,
            content_type=ContentType.objects.get(model='costcenter'),
            object_id=CostCenter.objects.get(name='SET').id)
        filter_set_can_see_customorders_with_cost_center_set.save()

        # Add a configuration
        config = Configuration(maintenance=False)
        config.save()

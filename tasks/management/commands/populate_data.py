from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from decimal import Decimal
from tasks.models import ArmoryCategory, Supplier, Weapon, Client, Transaction, IntelligenceNote

class Command(BaseCommand):
    help = 'Populates the database with classified arms dealing data'

    def handle(self, *args, **options):
        # 1. Categories
        categories_data = [
            {'name': 'Sidearms', 'description': 'Handguns and personal defense weapons.'},
            {'name': 'Assault Rifles', 'description': 'Standard issue military grade rifles.'},
            {'name': 'Sniper Systems', 'description': 'Long-range precision hardware.'},
            {'name': 'Heavy Ordinance', 'description': 'Explosives and anti-tank systems.'},
            {'name': 'Stealth Gear', 'description': 'Silenced and tactical infiltration tools.'},
        ]
        categories = []
        for c in categories_data:
            cat, _ = ArmoryCategory.objects.get_or_create(name=c['name'], defaults={'description': c['description']})
            categories.append(cat)

        # 2. Suppliers
        suppliers_data = [
            {'name': 'Stark Industries', 'country': 'USA', 'reliability_score': 98},
            {'name': 'Hammer Tech', 'country': 'USA', 'reliability_score': 45},
            {'name': 'Kalashnikov Concern', 'country': 'Russia', 'reliability_score': 95},
            {'name': 'Heckler & Koch', 'country': 'Germany', 'reliability_score': 99},
            {'name': 'Blackwater Logistics', 'country': 'International', 'reliability_score': 80},
        ]
        suppliers = []
        for s in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(name=s['name'], defaults=s)
            suppliers.append(sup)

        # 3. Weapons
        weapons_names = ['Interceptor', 'Shadow', 'Ghost', 'Raptor', 'Viper', 'Cobra', 'Titan', 'Colossus', 'Sentinel', 'Reaper']
        weapons = []
        for i in range(15):
            name = f"{random.choice(weapons_names)} {random.choice(['Mark I', 'V2', 'X-Series', 'Tactical'])}"
            model = f"AR-{random.randint(1000, 9999)}-{i}"
            weapon = Weapon.objects.create(
                name=name,
                model_number=model,
                category=random.choice(categories),
                supplier=random.choice(suppliers),
                caliber=random.choice(['9mm', '5.56mm', '7.62mm', '.50 BMG', 'HE']),
                unit_price=Decimal(random.randint(500, 25000)),
                stock_quantity=random.randint(5, 100),
                is_active=True
            )
            weapons.append(weapon)

        # 4. Clients
        clients_data = [
            {'name': 'The Resistance', 'region': 'Eastern Europe', 'clearance_level': 3},
            {'name': 'Global Peacekeepers', 'region': 'North America', 'clearance_level': 5},
            {'name': 'Shadow Syndicate', 'region': 'Unknown', 'clearance_level': 1},
            {'name': 'Desert Eagles', 'region': 'Middle East', 'clearance_level': 2},
            {'name': 'Cyber Dynes', 'region': 'Asia Pacific', 'clearance_level': 4},
        ]
        clients = []
        for cl in clients_data:
            client, _ = Client.objects.get_or_create(name=cl['name'], defaults=cl)
            clients.append(client)

        # 5. Transactions
        statuses = ["Pending", "Processing", "Completed", "Cancelled"]
        for i in range(25):
            weapon = random.choice(weapons)
            qty = random.randint(1, 10)
            deal = Transaction.objects.create(
                client=random.choice(clients),
                weapon=weapon,
                quantity=qty,
                total_price=weapon.unit_price * qty,
                status=random.choice(statuses),
                deal_date=timezone.now() - timezone.timedelta(days=random.randint(0, 30))
            )

            # 6. Intel Notes
            if random.random() < 0.6:
                IntelligenceNote.objects.create(
                    transaction=deal,
                    content=f"Classified intelligence briefing for transaction #{deal.id}. Target region: {deal.client.region}."
                )

        self.stdout.write(
            self.style.SUCCESS('ARSENAL Armory mainframe successfully populated with classified data!')
        )
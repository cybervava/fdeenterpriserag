from pathlib import Path
import random


random.seed(42)

BASE_DIR = Path("data/knowledge_base")

CATEGORIES = [
    "products",
    "case_studies",
    "integrations",
    "compliance",
    "industry_solutions",
    "comparisons",
    "faq",
]


for category in CATEGORIES:
    (BASE_DIR / category).mkdir(
        parents=True,
        exist_ok=True
    )


def save_document(category, filename, content):
    path = BASE_DIR / category / filename
    path.write_text(content.strip(), encoding="utf-8")


# --------------------------------------------------
# PRODUCT SPECIFICATIONS
# --------------------------------------------------

products = {
    "novasense_x100_technical_specification.txt": """
NovaTech Industrial Solutions
NovaSense X100 Technical Specification

Product: NovaSense X100

The NovaSense X100 is designed primarily for environmental
temperature monitoring in industrial environments.

Operating temperature range: -10°C to 70°C.
Maximum supported humidity: 80%.

Communication protocols:
- Modbus TCP
- MQTT

The X100 is appropriate for applications requiring basic
environmental temperature visibility and remote monitoring.
""",

    "novasense_x200_technical_specification.txt": """
NovaTech Industrial Solutions
NovaSense X200 Technical Specification
Product: NovaSense X200

The NovaSense X200 provides basic industrial condition
monitoring using vibration and temperature sensing.

Operating temperature range: -20°C to 80°C.
Maximum supported humidity: 90%.
Maximum vibration sampling rate: 10 kHz.

Communication protocols:
- Modbus
- MQTT
- Ethernet

The X200 is suitable for general condition-monitoring
applications where basic vibration and temperature
information is required.
""",

    "novasense_x500_technical_specification.txt": """
NovaTech Industrial Solutions
NovaSense X500 Technical Specification

Product: NovaSense X500

The NovaSense X500 is an advanced industrial predictive
maintenance platform designed for monitoring rotating
equipment including motors, pumps and compressors.

Supported capabilities include:
- Continuous vibration monitoring
- Temperature monitoring
- Anomaly detection
- Predictive maintenance
- Historical equipment-health trends

Operating temperature range: -20°C to 90°C.
Maximum supported humidity: 95%.
Maximum vibration sampling rate: 20 kHz.

Communication protocols:
- OPC-UA
- Modbus TCP
- MQTT
- Ethernet

The X500 is commonly deployed in automotive,
pharmaceutical, manufacturing and energy environments.
""",

    "novasense_x700_technical_specification.txt": """
NovaTech Industrial Solutions
NovaSense X700 Technical Specification

Product: NovaSense X700

The NovaSense X700 is designed for enterprise-scale
monitoring of critical industrial assets.

The platform provides advanced condition monitoring,
high-frequency data acquisition and edge analytics for
large industrial deployments.

Operating temperature range: -30°C to 100°C.
Maximum supported humidity: 95%.
Maximum vibration sampling rate: 30 kHz.

Communication protocols:
- OPC-UA
- Modbus
- MQTT
- Ethernet

The X700 is intended for organizations requiring
large-scale monitoring of critical equipment.
"""
}


for filename, content in products.items():
    save_document(
        "products",
        filename,
        content
    )


# --------------------------------------------------
# CASE STUDIES
# --------------------------------------------------

industries = [
    "Automotive Manufacturing",
    "Pharmaceutical Manufacturing",
    "Energy",
    "Industrial Manufacturing",
    "Chemical Processing",
]

assets = [
    "motors",
    "pumps",
    "compressors",
    "production equipment",
    "rotating equipment",
]


for i in range(1, 61):

    industry = random.choice(industries)
    asset = random.choice(assets)

    content = f"""
NovaTech Customer Case Study {i}

Industry: {industry}

A customer operating in the {industry} sector wanted to
improve visibility into the condition of its {asset}.

NovaTech industrial monitoring technology was deployed
to collect equipment temperature, vibration and health
information.

The monitoring solution allowed maintenance teams to
identify abnormal operating patterns earlier and improve
maintenance planning.

Predictive maintenance information helped engineering
teams reduce dependence on purely reactive maintenance.

This case demonstrates how industrial sensor information
can support equipment reliability and maintenance
decision-making.
"""

    save_document(
        "case_studies",
        f"case_study_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# INTEGRATION GUIDES
# --------------------------------------------------

systems = [
    ("Siemens SCADA", "OPC-UA"),
    ("Industrial MQTT Broker", "MQTT"),
    ("Manufacturing Execution System", "OPC-UA"),
    ("Plant Historian", "OPC-UA"),
    ("Industrial Gateway", "Modbus TCP"),
]

for i in range(1, 41):

    system, protocol = systems[(i - 1) % len(systems)]

    content = f"""
NovaTech Integration Guide {i}

Integration Target: {system}

NovaTech industrial monitoring products can exchange
equipment information with {system} using {protocol}
where supported by the selected NovaSense product.

Typical integration information includes equipment
temperature, vibration measurements, equipment-health
information and monitoring events.

For advanced predictive-maintenance deployments,
NovaSense X500 supports OPC-UA, Modbus TCP, MQTT and
Ethernet connectivity.

Integration architecture should be validated against
the customer's industrial network and security
requirements before production deployment.
"""

    save_document(
        "integrations",
        f"integration_guide_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# COMPLIANCE DOCUMENTS
# --------------------------------------------------

for i in range(1, 31):

    content = f"""
NovaTech Compliance Guidance {i}

NovaTech industrial monitoring deployments may operate
in regulated manufacturing environments.

Organizations should consider access control, audit
logging, data retention, network security and change
management when deploying monitoring infrastructure.

Pharmaceutical and other regulated environments may
require additional validation and documented operating
procedures.
Compliance obligations depend on the customer's
industry, jurisdiction and internal governance
requirements.

NovaTech solutions should therefore be deployed as part
of the customer's broader compliance and security
architecture.
"""

    save_document(
        "compliance",
        f"compliance_guidance_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# INDUSTRY SOLUTIONS
# --------------------------------------------------

industry_names = [
    "Automotive Manufacturing",
    "Pharmaceutical Manufacturing",
    "Energy",
    "General Manufacturing",
    "Chemical Processing",
]


for i in range(1, 101):

    industry = industry_names[
        (i - 1) % len(industry_names)
    ]

    content = f"""
NovaTech {industry} Solution {i}

NovaTech provides industrial equipment-monitoring
solutions for organizations operating in
{industry}.

Typical deployments monitor equipment temperature,
vibration and asset-health information.

Predictive maintenance can help maintenance teams
identify abnormal equipment behavior before a
significant failure occurs.

The NovaSense X500 is designed for advanced predictive
maintenance of motors, pumps, compressors and other
rotating industrial equipment.
Sensor information can be integrated into broader
industrial monitoring and maintenance workflows.
"""

    save_document(
        "industry_solutions",
        f"{industry.lower().replace(' ', '_')}_solution_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# PRODUCT COMPARISONS
# --------------------------------------------------

for i in range(1, 31):

    content = f"""
NovaTech Product Comparison {i}

NovaSense X100 focuses primarily on environmental
temperature monitoring.

NovaSense X200 provides basic condition monitoring
using vibration and temperature sensing.

NovaSense X500 provides advanced predictive-maintenance
capabilities for motors, pumps, compressors and other
rotating equipment.

NovaSense X700 is intended for enterprise-scale
monitoring of critical industrial assets and provides
higher-frequency acquisition and edge capabilities.

Product selection should be based on monitoring
requirements, integration requirements and deployment
scale.
"""

    save_document(
        "comparisons",
        f"product_comparison_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# FAQ DOCUMENTS
# --------------------------------------------------

for i in range(1, 31):
    content = f"""
NovaTech Product FAQ {i}

Q: Which NovaSense product supports advanced predictive
maintenance?

A: NovaSense X500 is designed for advanced predictive
maintenance of industrial rotating equipment.

Q: Which products support MQTT?

A: MQTT is supported by multiple NovaSense products,
including X100, X200, X500 and X700.

Q: Can NovaSense products integrate with industrial
systems?

A: Supported products provide industrial communication
options including OPC-UA, Modbus, MQTT and Ethernet.

Q: What should customers verify before deployment?

A: Customers should validate environmental,
connectivity, security and application requirements
against the selected product specification.
"""

    save_document(
        "faq",
        f"faq_{i:03d}.txt",
        content
    )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

total_files = len(
    list(BASE_DIR.rglob("*.txt"))
)

print("=" * 60)
print("NOVATECH ENTERPRISE DATASET GENERATED")
print("=" * 60)

for category in CATEGORIES:

    count = len(
        list(
            (BASE_DIR / category).glob("*.txt")
        )
    )

    print(f"{category:20s}: {count}")

print("-" * 60)
print("Total documents:", total_files)

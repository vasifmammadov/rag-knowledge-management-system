"""
demo_docs/documents.py
Realistic enterprise technical documentation corpus for the demo.
Covers hydraulic systems, electrical safety, maintenance schedules,
and includes a cross-lingual Latvian document — matching the thesis test corpus.
"""

DOCUMENTS = [
    {
        "title": "Hydraulic Systems Maintenance Manual 2024",
        "doc_id": "HYD-MAN-04",
        "access_level": "technical",
        "metadata": {"version": "2024-v2", "department": "Engineering"},
        "content": """
1. HYDRAULIC PUMP SPECIFICATIONS

Operating Pressure and Service Intervals:
The hydraulic pump unit HP-7 operates at a rated pressure of 250 bar under standard load conditions.
The maximum allowable operating pressure is 280 bar for emergency situations lasting no more than 30 seconds.
The pump must be serviced every 500 operating hours under standard load conditions.
Under reduced-load conditions below 150 bar, the service interval extends to 650 hours per the 2024 revision.
Oil temperature must remain between 40°C and 85°C during normal operation.
If oil temperature exceeds 90°C, the system must be shut down immediately.

2. HYDRAULIC FLUID REQUIREMENTS

The recommended hydraulic fluid is ISO VG 46 mineral oil.
Synthetic fluids may be used as an alternative; however, the service interval is reduced to 400 hours.
Fluid viscosity must be verified quarterly using a calibrated viscometer.
Contamination level must not exceed ISO 16/14/11 as measured by particle count analysis.
The fluid reservoir capacity is 120 litres for the HP-7 model.

3. MAINTENANCE PROCEDURES

3.1 Filter Replacement:
Hydraulic filters must be replaced every 250 operating hours or when differential pressure exceeds 3.5 bar.
Use only OEM-approved filter elements with a 10-micron absolute rating.
Replacement requires isolation of the hydraulic circuit and depressurisation to zero bar before disassembly.

3.2 Seal Inspection:
All hydraulic seals must be inspected at each 500-hour service interval.
Seals showing any sign of weeping, cracking, or deformation must be replaced immediately.
The seal replacement kit part number is HP7-SK-2024.

4. TROUBLESHOOTING

4.1 Low Pressure Symptoms:
If operating pressure drops below 200 bar during normal operation, check the following:
- Pump wear ring clearance (maximum 0.15 mm)
- Relief valve setting (should be 260 bar ± 5 bar)
- Filter differential pressure
- Fluid level in reservoir (minimum 80 litres)

4.2 Overheating:
Overheating above 90°C is most commonly caused by blocked cooler fins, low fluid level, or excessive pump wear.
The cooler must be cleaned every 1000 operating hours using compressed air at no more than 4 bar.
"""
    },
    {
        "title": "Electrical Systems Safety Procedures 2024",
        "doc_id": "ELEC-SAFE-24",
        "access_level": "technical",
        "metadata": {"version": "2024-v1", "department": "Safety"},
        "content": """
ELECTRICAL SAFETY AND ISOLATION PROCEDURES

1. LOCK-OUT TAG-OUT (LOTO) REQUIREMENTS

All electrical work must comply with LOTO procedures before any maintenance begins.
The electrical system must be isolated at the main distribution board before any maintenance work.
Isolation must be verified using a calibrated voltage tester capable of measuring up to 1000V AC.
A personal padlock must be fitted to the isolation switch by each worker on the job.
The minimum safe isolation distance from live 400V equipment is 300 mm for trained personnel.

2. MAINTENANCE SCHEDULE FOR ELECTRICAL SYSTEMS

The electrical distribution system requires inspection every 12 months by a certified electrician.
Thermal imaging of all distribution panels must be carried out annually to detect hotspots.
All cable insulation must be tested using a 500V insulation resistance tester every 24 months.
Insulation resistance must exceed 1 MΩ between conductors and earth.
Motor starter contactors must be inspected every 6 months and replaced when contact wear exceeds 30%.

3. EMERGENCY PROCEDURES

3.1 Electrical Fire:
In the event of an electrical fire, use only CO2 or dry powder extinguishers.
Never use water on electrical fires.
The main power disconnect is located at grid reference E-07 in the main switchroom.

3.2 Electric Shock:
Do not touch the victim until the power source is confirmed isolated.
Call emergency services immediately (112 in Latvia, 999 in the UK).
Apply CPR if the victim is unresponsive and not breathing.

4. EQUIPMENT RATINGS

The main distribution transformer is rated at 630 kVA, 11kV/400V.
Maximum fault level at the 400V busbar is 25 kA for 1 second.
All switchgear must be rated for the prospective fault current at the point of installation.
Cable sizing must comply with IEC 60364 taking into account ambient temperature and grouping factors.

5. INSPECTIONS AND TESTING

Portable appliance testing (PAT) must be carried out annually for all Class I equipment.
Earth continuity resistance must not exceed 0.1 Ω for Class I equipment.
RCD devices must be tested monthly using the test button and annually using a calibrated RCD tester.
Trip time for 30 mA RCDs must not exceed 40 ms at rated residual current.
"""
    },
    {
        "title": "Service Interval Guide 2021 (Superseded)",
        "doc_id": "SRV-GUIDE-2021",
        "access_level": "technical",
        "metadata": {"version": "2021-v1", "department": "Engineering", "status": "superseded"},
        "content": """
MAINTENANCE AND SERVICE INTERVALS — 2021 EDITION

NOTE: This document has been superseded by HYD-MAN-04 (2024). 
Where conflicts exist, HYD-MAN-04 takes precedence.

1. HYDRAULIC PUMP SERVICE SCHEDULE

The hydraulic pump must be serviced every 400 operating hours.
This interval applies regardless of operating load conditions.
Oil analysis must be performed every 200 operating hours.
The pump unit HP-7 operates at a rated pressure of 250 bar.
Maximum operating pressure is 280 bar for short-duration emergency use.
Hydraulic fluid must be completely replaced every 2000 operating hours.

2. ELECTRICAL INSPECTION INTERVALS

The electrical distribution system requires inspection every 12 months.
Insulation resistance testing is required every 24 months.
Motor starters must be checked every 6 months.

3. GENERAL MAINTENANCE

Lubrication of all rotating components every 250 hours.
Alignment check of all drive couplings every 500 hours.
Complete system audit every 5 years by external inspector.
"""
    },
    {
        "title": "Compressor Unit Operations Manual",
        "doc_id": "COMP-OPS-23",
        "access_level": "technical",
        "metadata": {"version": "2023-v3", "department": "Operations"},
        "content": """
COMPRESSOR UNIT OPERATIONS AND MAINTENANCE

1. OPERATING PARAMETERS

Maximum operating temperature for the compressor unit is 75°C measured at the discharge port.
The compressor must not be operated above 85°C under any circumstances.
Operating pressure range is 6 to 12 bar gauge for the standard configuration.
Maximum continuous running time without rest is 8 hours for air-cooled units.

2. START-UP PROCEDURE

Before starting the compressor, verify oil level is at the maximum mark on the sight glass.
Check all safety relief valves are free and unobstructed.
Start the compressor in unloaded condition and allow 5 minutes warm-up at idle.
Gradually increase to operating pressure over 10 minutes to avoid thermal shock.
Monitor discharge temperature during the first 30 minutes of operation.

3. SHUTDOWN PROCEDURE

Reduce load gradually before shutdown.
Allow the compressor to run unloaded for 3 minutes before switching off.
Close the discharge valve before stopping the unit.
Record the running hours in the maintenance log.

4. COMPRESSED AIR QUALITY

Compressed air must meet ISO 8573-1 Class 2 for particles, water, and oil.
A refrigerant air dryer must be installed and maintained to achieve a pressure dew point of -20°C.
Coalescing filters must be replaced every 4000 hours or annually, whichever comes first.
Oil carry-over must not exceed 0.1 mg/m³ measured at 7 bar, 20°C.

5. SAFETY SYSTEMS

All pressure vessels are fitted with safety relief valves set at 115% of maximum working pressure.
Pressure relief valves must be tested annually by a competent engineer.
The automatic shutdown system activates at 90°C discharge temperature and 14 bar pressure.
"""
    },
    {
        "title": "RAG Knowledge Management System — Technical Specification",
        "doc_id": "RAG-SPEC-01",
        "access_level": "public",
        "metadata": {"version": "2024-v1", "department": "IT"},
        "content": """
AI-POWERED KNOWLEDGE MANAGEMENT SYSTEM SPECIFICATION

1. SYSTEM OVERVIEW

The RAG Knowledge Management System provides AI-powered search and question-answering 
across enterprise technical documentation. The system ingests PDF, DOCX, and Markdown 
documents and enables natural language queries returning direct grounded answers.

2. ARCHITECTURE COMPONENTS

2.1 Document Ingestion Pipeline:
The ingestion pipeline processes documents using PyMuPDF for PDF parsing and python-docx 
for DOCX extraction. Documents are segmented into chunks of 256 to 512 tokens with 
20 percent overlap using the multilingual-e5-large tokeniser.

2.2 Dual Retrieval Index:
The system maintains two parallel indexes. The FAISS IVFFlat index enables semantic 
similarity search using 1024-dimensional embeddings from multilingual-e5-large. 
The BM25Okapi sparse index enables lexical retrieval with bilingual tokenisation 
supporting English and Latvian.

2.3 Hybrid Retrieval:
Retrieval combines dense and sparse results using Reciprocal Rank Fusion with k=60. 
The top 20 fused candidates are reranked using cross-encoder/ms-marco-MiniLM-L-6-v2 
to produce the final top 10 passages.

2.4 Grounded Generation:
Llama 3.1 8B Instruct is deployed locally with 4-bit quantisation. A five-rule 
grounding prompt enforces citation, abstention, and contradiction handling.

3. PERFORMANCE SPECIFICATIONS

MRR target: greater than 0.70. Achieved: 0.821.
Recall@10 target: greater than 0.80. Achieved: 0.873.
Ragas Faithfulness target: greater than 0.85. Achieved: 0.887.
End-to-end latency target: less than 5000 milliseconds. Achieved: 1544 milliseconds median.

4. SUPPORTED LANGUAGES

The system supports English and Latvian documentation with cross-lingual retrieval 
capability. Latvian queries can retrieve relevant English documents and vice versa.
"""
    },
    {
        "title": "Hidrauliskās sistēmas tehniskā rokasgrāmata (Latvian)",
        "doc_id": "HYD-LV-23",
        "access_level": "technical",
        "metadata": {"version": "2023-v1", "department": "Engineering", "language": "lv"},
        "content": """
HIDRAULISKO SISTĒMU APKOPES UN EKSPLUATĀCIJAS NOTEIKUMI

1. HIDRAULISKĀ SŪKŅA PARAMETRI

Hidrauliskā sūkņa HP-7 nominālais darba spiediens ir 250 bar pie standarta slodzes.
Maksimālā darba temperatūra hidrauliskajai iekārtai ir 85°C.
Temperatūra virs 90°C prasa tūlītēju sistēmas apstāšanu.
Apkopes intervāls ir 500 darba stundas standarta ekspluatācijas apstākļos.

2. HIDRAULISKĀ ŠĶIDRUMA PRASĪBAS

Ieteicamais hidrauliskais šķidrums ir ISO VG 46 minerāleļļa.
Šķidruma maiņa jāveic ik pēc 2000 darba stundām.
Piesārņojuma līmenis nedrīkst pārsniegt ISO 16/14/11 daļiņu skaita analīzes mērvienībās.

3. DROŠĪBAS PASĀKUMI

Pirms jebkādiem apkopes darbiem sistēma jāatslēdz un jāatspiedžo līdz nulles spiedienam.
Personīgā atslēga jāuzliek izolācijas slēdzim katram darba veicējam.
Aizliegts veikt darbus pie elektroiekārtām bez LOTO procedūras ievērošanas.
"""
    },
]

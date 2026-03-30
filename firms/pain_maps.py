"""Problem-domain mappings for Prompt #02 B2B scoring."""

from __future__ import annotations


OFFER_TO_FIRM_PAIN_FIELD = {
    "customer_support": "avg_need_customer_support",
    "document_admin": "avg_need_document_admin",
    "sales_marketing": "avg_need_sales_marketing",
    "collections": "avg_need_collections",
    "ops_scheduling": "avg_need_ops_scheduling",
    "hr_internal": "avg_need_hr_internal",
    "healthcare_screening": "avg_need_document_admin",
}


SECTOR_PAIN_NOTES = {
    "retail_trade": "Customer support, sales conversion, and cash-cycle friction are the main modeled AI pain points.",
    "food_service": "Demand spikes and order coordination make workflow and response-time tools more relevant.",
    "healthcare_services": "Documentation, compliance, and front-desk speed matter more than entertainment-style AI.",
    "education_services": "Collections, learner communications, and content support matter more than full ERP replacement.",
    "logistics_services": "Dispatch and collections pressure dominate.",
    "professional_services": "Document throughput and internal productivity dominate.",
    "light_manufacturing": "Scheduling and collections matter more than generative marketing.",
    "tourism_hospitality": "Booking response speed and multilingual front-desk service matter.",
}

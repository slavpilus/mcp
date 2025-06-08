@mcp.tool()
def get_return_policy(product_category: Optional[str] = None) -> Dict[str, Any]:
    """
    Get comprehensive return and refund policy information.

    Args:
        product_category: Optional specific category (electronics, clothing, books, etc.)
    """

    base_policy = {
        "standard_return_window": "30 days",
        "condition_requirements": [
            "Items must be unused and in original condition",
            "Original packaging and tags must be included",
            "Receipt or order confirmation required"
        ],
        "refund_timeframe": "3-5 business days after we receive returned item",
        "return_shipping": "Free prepaid return labels provided",
        "restocking_fee": "None for standard items"
    }

    category_specific = {
        "electronics": {
            "return_window": "15 days",
            "special_conditions": ["Software must be unopened", "Original accessories required"],
            "restocking_fee": "10% for opened items"
        },
        "clothing": {
            "return_window": "45 days",
            "special_conditions": ["Must not show signs of wear", "Hygiene items non-returnable"],
            "size_exchange": "Free size exchanges within 60 days"
        },
        "books": {
            "return_window": "30 days",
            "special_conditions": ["Must be in resellable condition", "No writing or highlighting"],
            "digital_content": "Digital books non-returnable after download"
        },
        "custom_items": {
            "return_window": "Non-returnable",
            "special_conditions": ["Made-to-order items cannot be returned"],
            "exceptions": "Defective items eligible for replacement"
        }
    }

    result = {"general_policy": base_policy}

    if product_category and product_category.lower() in category_specific:
        result["category_specific"] = category_specific[product_category.lower()]
        result["customer_service_notes"] = [
            f"For {product_category} items, note the different return window",
            "Always mention special conditions upfront",
            "Offer alternatives if return isn't possible"
        ]

    result["helpful_tips"] = [
        "Start return process online for fastest service",
        "Take photos if item arrived damaged",
        "Keep tracking number for return shipment",
        "Refunds process faster than exchanges"
    ]

    result["escalation_triggers"] = [
        "Customer claims item was defective on arrival",
        "Return request after policy window expires",
        "Dispute over item condition assessment"
    ]

    return result

# =============================================================================
# 2. SHIPPING INFORMATION - Second most common inquiry
# =============================================================================

@mcp.tool()
def get_shipping_info(destination_country: Optional[str] = None, order_value: Optional[float] = None) -> Dict[str, Any]:
    """
    Get shipping options, costs, and delivery timeframes.

    Args:
        destination_country: Country for international shipping info
        order_value: Order value to check for free shipping eligibility
    """

    domestic_shipping = {
        "standard_shipping": {
            "cost": "$5.99",
            "timeframe": "5-7 business days",
            "description": "Ground shipping via USPS/UPS"
        },
        "expedited_shipping": {
            "cost": "$12.99",
            "timeframe": "2-3 business days",
            "description": "Priority shipping"
        },
        "overnight_shipping": {
            "cost": "$24.99",
            "timeframe": "Next business day",
            "description": "Express overnight delivery"
        },
        "free_shipping": {
            "threshold": 75.00,
            "conditions": "Standard shipping on orders $75+",
            "exclusions": ["Oversized items", "Remote areas"]
        }
    }

    international_rates = {
        "canada": {"standard": "$15.99", "expedited": "$29.99", "timeframe": "7-14 days"},
        "uk": {"standard": "$19.99", "expedited": "$39.99", "timeframe": "10-21 days"},
        "australia": {"standard": "$24.99", "expedited": "$49.99", "timeframe": "14-28 days"},
        "europe": {"standard": "$22.99", "expedited": "$44.99", "timeframe": "12-25 days"}
    }

    result = {
        "domestic_options": domestic_shipping,
        "processing_time": "1-2 business days before shipment",
        "cutoff_times": {
            "standard": "2 PM EST for same-day processing",
            "expedited": "12 PM EST for same-day processing",
            "overnight": "10 AM EST for same-day processing"
        }
    }

    # Add free shipping eligibility check
    if order_value is not None:
        free_shipping_eligible = order_value >= 75.00
        result["free_shipping_eligible"] = free_shipping_eligible
        result["customer_guidance"] = (
            f"Order qualifies for free shipping!" if free_shipping_eligible
            else f"Add ${75.00 - order_value:.2f} more for free shipping"
        )

    # Add international info if requested
    if destination_country:
        country_key = destination_country.lower()
        if country_key in international_rates:
            result["international_shipping"] = international_rates[country_key]
            result["international_notes"] = [
                "Duties and taxes may apply at destination",
                "Delivery times may vary due to customs processing",
                "Tracking available until item reaches destination country"
            ]
        else:
            result["international_shipping"] = "Contact support for rates to this destination"

    result["shipping_restrictions"] = [
        "No delivery to PO Boxes for expedited/overnight",
        "Some items cannot ship to APO/FPO addresses",
        "Hazardous materials have shipping restrictions"
    ]

    return result

# =============================================================================
# 3. CONTACT INFORMATION - Essential for escalations
# =============================================================================

@mcp.tool()
def get_contact_information(issue_type: Optional[str] = None, urgency: Optional[str] = "normal") -> Dict[str, Any]:
    """
    Get customer service contact information based on issue type and urgency.

    Args:
        issue_type: Type of issue (billing, technical, returns, general)
        urgency: Urgency level (low, normal, high, emergency)
    """

    general_contact = {
        "phone": "1-800-SUPPORT (1-800-786-7678)",
        "email": "support@example.com",
        "live_chat": "Available on website 24/7",
        "business_hours": {
            "phone_support": "Monday-Friday 8 AM - 8 PM EST, Saturday 9 AM - 5 PM EST",
            "email_response": "Within 24 hours on business days",
            "chat_response": "Average wait time: 3-5 minutes"
        }
    }

    specialized_contacts = {
        "billing": {
            "department": "Billing & Payments",
            "phone": "1-800-BILLING (1-800-245-5464)",
            "email": "billing@example.com",
            "hours": "Monday-Friday 9 AM - 6 PM EST",
            "notes": "Have your order number and billing zip code ready"
        },
        "technical": {
            "department": "Technical Support",
            "phone": "1-800-TECH-HELP (1-800-832-4435)",
            "email": "tech@example.com",
            "hours": "24/7 phone support available",
            "notes": "Screen sharing available for complex issues"
        },
        "returns": {
            "department": "Returns & Exchanges",
            "phone": "Use general support number",
            "email": "returns@example.com",
            "online_portal": "https://example.com/returns",
            "notes": "Online portal fastest for return requests"
        },
        "corporate": {
            "department": "Corporate Relations",
            "email": "corporate@example.com",
            "mail": "123 Example Street, Business City, ST 12345",
            "notes": "For formal complaints and business inquiries"
        }
    }

    urgency_guidance = {
        "emergency": {
            "recommended_contact": "phone",
            "note": "Call immediately for security issues or fraudulent charges",
            "escalation": "Ask for supervisor if wait time exceeds 5 minutes"
        },
        "high": {
            "recommended_contact": "phone or live_chat",
            "note": "Order issues within 24 hours of delivery",
            "escalation": "Mention high priority when contacting"
        },
        "normal": {
            "recommended_contact": "live_chat or email",
            "note": "Most issues resolved within normal timeframes"
        },
        "low": {
            "recommended_contact": "email",
            "note": "Non-urgent questions, feedback, suggestions"
        }
    }

    result = {"general_contact": general_contact}

    if issue_type and issue_type.lower() in specialized_contacts:
        result["specialized_contact"] = specialized_contacts[issue_type.lower()]
        result["routing_advice"] = f"Route to {specialized_contacts[issue_type.lower()]['department']} for faster resolution"

    if urgency in urgency_guidance:
        result["urgency_guidance"] = urgency_guidance[urgency]

    result["self_service_options"] = [
        "Order tracking: example.com/track",
        "FAQ:   example.com/help",
        "Return portal: example.com/returns",
        "Account management: example.com/account"
    ]

    result["customer_service_tips"] = [
        "Have order number ready before calling",
        "Take note of representative name and reference number",
        "For complex issues, email may provide better documentation"
    ]

    return result

# =============================================================================
# 4. SIZE GUIDE - Critical for clothing/footwear
# =============================================================================

@mcp.tool()
def get_size_guide(product_type: str, brand: Optional[str] = None) -> Dict[str, Any]:
    """
    Get size guide information for clothing, shoes, and accessories.

    Args:
        product_type: Type of product (shirts, pants, shoes, dresses, etc.)
        brand: Specific brand if sizing varies by brand
    """

    size_charts = {
        "shirts": {
            "mens": {
                "XS": {"chest": "32-34", "waist": "26-28"},
                "S": {"chest": "34-36", "waist": "28-30"},
                "M": {"chest": "38-40", "waist": "32-34"},
                "L": {"chest": "42-44", "waist": "36-38"},
                "XL": {"chest": "46-48", "waist": "40-42"},
                "XXL": {"chest": "50-52", "waist": "44-46"}
            },
            "womens": {
                "XS": {"bust": "30-32", "waist": "24-26", "hips": "34-36"},
                "S": {"bust": "32-34", "waist": "26-28", "hips": "36-38"},
                "M": {"bust": "34-36", "waist": "28-30", "hips": "38-40"},
                "L": {"bust": "36-38", "waist": "30-32", "hips": "40-42"},
                "XL": {"bust": "38-40", "waist": "32-34", "hips": "42-44"}
            }
        },
        "shoes": {
            "mens": {
                "7": {"us": "7", "uk": "6", "eu": "40", "cm": "25"},
                "8": {"us": "8", "uk": "7", "eu": "41", "cm": "26"},
                "9": {"us": "9", "uk": "8", "eu": "42", "cm": "27"},
                "10": {"us": "10", "uk": "9", "eu": "43", "cm": "28"},
                "11": {"us": "11", "uk": "10", "eu": "44", "cm": "29"},
                "12": {"us": "12", "uk": "11", "eu": "45", "cm": "30"}
            },
            "womens": {
                "6": {"us": "6", "uk": "4", "eu": "36", "cm": "22.5"},
                "7": {"us": "7", "uk": "5", "eu": "37", "cm": "23.5"},
                "8": {"us": "8", "uk": "6", "eu": "38", "cm": "24.5"},
                "9": {"us": "9", "uk": "7", "eu": "39", "cm": "25.5"},
                "10": {"us": "10", "uk": "8", "eu": "40", "cm": "26.5"}
            }
        },
        "dresses": {
            "sizes": {
                "XS": {"bust": "30-32", "waist": "24-26", "hips": "34-36", "length": "Variable by style"},
                "S": {"bust": "32-34", "waist": "26-28", "hips": "36-38", "length": "Variable by style"},
                "M": {"bust": "34-36", "waist": "28-30", "hips": "38-40", "length": "Variable by style"},
                "L": {"bust": "36-38", "waist": "30-32", "hips": "40-42", "length": "Variable by style"}
            }
        }
    }

    measuring_instructions = {
        "chest_bust": "Measure around the fullest part of chest/bust, keeping tape parallel to floor",
        "waist": "Measure around natural waistline, keeping one finger between body and tape",
        "hips": "Measure around fullest part of hips, about 7-9 inches below waist",
        "inseam": "Measure from crotch to bottom of ankle along inside leg",
        "foot_length": "Stand on paper, mark heel and longest toe, measure distance"
    }

    result = {"measuring_instructions": measuring_instructions}

    if product_type.lower() in size_charts:
        result["size_chart"] = size_charts[product_type.lower()]
        result["product_specific_notes"] = {
            "shirts": "Consider preferred fit - slim, regular, or relaxed",
            "shoes": "Sizes may vary between athletic and dress shoes",
            "dresses": "Check specific measurements as styles vary significantly"
        }.get(product_type.lower(), "Refer to specific product measurements")


    if brand and brand.lower() in brand_variations:
        result["brand_specific_notes"] = brand_variations[brand.lower()]

    result["fitting_tips"] = [
        "When between sizes, size up for comfort",
        "Check fabric content - stretchy materials may fit differently",
        "Read customer reviews for fit feedback",
        "Consider your preferred fit style (tight, loose, regular)"
    ]

    result["exchange_policy"] = {
        "size_exchanges": "Free within 60 days",
        "condition": "Items must be unworn with tags attached",
        "process": "Use online exchange portal for fastest service"
    }

    return result

# =============================================================================
# 5. WARRANTY & GUARANTEE INFORMATION
# =============================================================================

@mcp.tool()
def get_warranty_information(product_category: str, purchase_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get warranty and guarantee information for products.

    Args:
        product_category: Category of product (electronics, appliances, furniture, etc.)
        purchase_date: Date of purchase to check warranty status (YYYY-MM-DD)
    """

    warranty_terms = {
        "electronics": {
            "standard_warranty": "1 year from purchase date",
            "coverage": ["Manufacturing defects", "Hardware failures", "Performance issues"],
            "exclusions": ["Physical damage", "Water damage", "Software issues", "Normal wear"],
            "extended_options": "Up to 3 years available at purchase",
            "repair_process": "Authorized service centers or mail-in repair"
        },
        "appliances": {
            "standard_warranty": "2 years parts and labor",
            "coverage": ["Manufacturing defects", "Motor failures", "Component malfunctions"],
            "exclusions": ["Misuse", "Normal wear items", "Cosmetic damage"],
            "extended_options": "Up to 5 years available",
            "repair_process": "In-home service or authorized repair centers"
        },
        "furniture": {
            "standard_warranty": "5 years structural, 2 years fabric/finish",
            "coverage": ["Frame defects", "Joint failures", "Spring systems"],
            "exclusions": ["Fabric wear", "Scratches", "Fading", "Pet damage"],
            "extended_options": "Fabric protection plans available",
            "repair_process": "In-home assessment and repair"
        },
        "clothing": {
            "standard_warranty": "90 days quality guarantee",
            "coverage": ["Seam failures", "Zipper defects", "Button attachment"],
            "exclusions": ["Normal wear", "Stains", "Shrinkage", "Color fading"],
            "extended_options": "Not available",
            "repair_process": "Return for replacement or store credit"
        }
    }

    result = {}

    if product_category.lower() in warranty_terms:
        warranty_info = warranty_terms[product_category.lower()]
        result["warranty_terms"] = warranty_info

        # Check warranty status if purchase date provided
        if purchase_date:
            try:
                from datetime import datetime, timedelta
                purchase_dt = datetime.strptime(purchase_date, "%Y-%m-%d")
                current_dt = datetime.now()
                days_since_purchase = (current_dt - purchase_dt).days

                # Extract warranty period (simplified)
                warranty_days = 365  # Default 1 year
                if "2 years" in warranty_info["standard_warranty"]:
                    warranty_days = 730
                elif "5 years" in warranty_info["standard_warranty"]:
                    warranty_days = 1825
                elif "90 days" in warranty_info["standard_warranty"]:
                    warranty_days = 90

                days_remaining = warranty_days - days_since_purchase

                result["warranty_status"] = {
                    "days_since_purchase": days_since_purchase,
                    "days_remaining": max(0, days_remaining),
                    "status": "Active" if days_remaining > 0 else "Expired",
                    "expiration_date": (purchase_dt + timedelta(days=warranty_days)).strftime("%Y-%m-%d")
                }

                if days_remaining <= 30 and days_remaining > 0:
                    result["urgent_notice"] = "Warranty expires soon - file any claims immediately"

            except ValueError:
                result["date_error"] = "Invalid date format. Please use YYYY-MM-DD."

    result["claim_process"] = {
        "requirements": [
            "Original receipt or order confirmation",
            "Product model/serial number",
            "Description of defect or issue",
            "Photos if applicable"
        ],
        "initiation": "Start claim online or call warranty department",
        "timeline": "Initial response within 2 business days",
        "resolution": "Repair, replacement, or refund as appropriate"
    }

    result["satisfaction_guarantee"] = {
        "period": "30 days from delivery",
        "coverage": "Not satisfied for any reason",
        "process": "Return for full refund",
        "condition": "Item must be in original condition"
    }

    result["customer_service_notes"] = [
        "Always ask for receipt/order number first",
        "Document warranty claim details thoroughly",
        "Escalate if customer reports safety issues",
        "Offer satisfaction guarantee if warranty expired recently"
    ]

    return result

# =============================================================================
# 6. PAYMENT METHODS & BILLING - Financial inquiries
# =============================================================================

@mcp.tool()
def get_payment_information(inquiry_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about accepted payment methods, billing, and financial policies.

    Args:
        inquiry_type: Type of payment inquiry (methods, billing, security, issues)
    """

    accepted_payments = {
        "credit_cards": {
            "accepted": ["Visa", "Mastercard", "American Express", "Discover"],
            "processing": "Charged when item ships",
            "security": "256-bit SSL encryption, PCI DSS compliant"
        },
        "digital_wallets": {
            "accepted": ["PayPal", "Apple Pay", "Google Pay", "Shop Pay"],
            "benefits": "Faster checkout, enhanced security",
            "processing": "Immediate authorization, charged at shipment"
        },
        "buy_now_pay_later": {
            "providers": ["Klarna", "Afterpay", "Sezzle"],
            "terms": "4 interest-free payments over 6 weeks",
            "eligibility": "Credit check required, minimum order $35"
        }
    }

    billing_information = {
        "when_charged": {
            "authorization": "When order is placed",
            "capture": "When item ships",
            "partial_shipments": "Charged as each item ships"
        },
        "billing_address": {
            "requirement": "Must match payment method address",
            "international": "Supported for most countries",
            "changes": "Update before order ships"
        },
        "receipts": {
            "email": "Sent automatically to order email",
            "printed": "Available in account dashboard",
            "business": "Detailed receipts for business customers"
        }
    }

    security_measures = {
        "fraud_protection": "Advanced fraud detection algorithms",
        "cvv_verification": "Required for all credit card transactions",
        "address_verification": "AVS check for billing address match",
        "secure_storage": "Payment information encrypted and tokenized",
        "pci_compliance": "PCI DSS Level 1 certified merchant"
    }

    common_issues = {
        "declined_cards": {
            "causes": ["Insufficient funds", "Expired card", "Billing address mismatch", "Bank fraud prevention"],
            "solutions": ["Verify card details", "Contact bank", "Try different payment method", "Update billing address"]
        },
        "duplicate_charges": {
            "explanation": "Authorization hold may appear as duplicate charge",
            "resolution": "Hold automatically releases in 3-5 business days",
            "action": "Contact us if charge posts twice"
        },
        "international_cards": {
            "requirements": "Enable international transactions with bank",
            "currencies": "Prices shown in USD, converted by card issuer",
            "fees": "Bank may charge foreign transaction fees"
        }
    }

    result = {
        "accepted_payments": accepted_payments,
        "billing_information": billing_information
    }

    if inquiry_type:
        if inquiry_type.lower() == "security":
            result["security_details"] = security_measures
        elif inquiry_type.lower() == "issues":
            result["troubleshooting"] = common_issues
        elif inquiry_type.lower() == "methods":
            result["detailed_methods"] = accepted_payments
        elif inquiry_type.lower() == "billing":
            result["billing_details"] = billing_information

    result["customer_service_guidance"] = [
        "For declined payments, always suggest contacting bank first",
        "Verify billing address matches payment method exactly",
        "Offer alternative payment methods if primary fails",
        "Escalate suspected fraud cases immediately"
    ]

    result["self_service_options"] = [
        "Update payment methods in account settings",
        "View billing history in order dashboard",
        "Download receipts from order confirmation emails",
        "Check gift card balances online"
    ]

    return result

# =============================================================================
# 7. ACCOUNT & LOGIN HELP - Technical support
# =============================================================================

@mcp.tool()
def get_account_help(issue_type: str) -> Dict[str, Any]:
    """
    Get help with account-related issues and login problems.

    Args:
        issue_type: Type of account issue (login, password, registration, profile, etc.)
    """

    login_troubleshooting = {
        "forgot_password": {
            "steps": [
                "Click 'Forgot Password' on login page",
                "Enter email address associated with account",
                "Check email for reset link (including spam folder)",
                "Follow link to create new password",
                "Password must be 8+ characters with special character"
            ],
            "common_issues": [
                "Email not received - check spam/junk folder",
                "Reset link expired - request new link",
                "Email address not recognized - try alternate emails"
            ]
        },
        "account_locked": {
            "causes": [
                "Too many failed login attempts",
                "Suspicious activity detected",
                "Password security requirements not met"
            ],
            "resolution": [
                "Wait 15 minutes for automatic unlock",
                "Use password reset if lock persists",
                "Contact support for immediate unlock"
            ]
        },
        "email_verification": {
            "process": [
                "Check email for verification message",
                "Click verification link in email",
                "Return to website to complete login",
                "Resend verification if email not received"
            ],
            "issues": [
                "Verification email in spam folder",
                "Link expired after 24 hours",
                "Email address typo during registration"
            ]
        }
    }

    account_management = {
        "profile_updates": {
            "editable_fields": ["Name", "Email", "Phone", "Addresses", "Communication preferences"],
            "restrictions": ["Email changes require verification", "Some changes affect active orders"],
            "process": "Account Settings > Profile > Edit Information"
        },
        "address_book": {
            "management": "Add, edit, or remove shipping addresses",
            "default_setting": "Set preferred billing and shipping addresses",
            "validation": "Addresses validated against postal service database"
        },
        "order_history": {
            "access": "View all past orders and their status",
            "actions": ["Reorder items", "Track packages", "Download receipts", "Request returns"],
            "retention": "Order history maintained for 7 years"
        }
    }

    security_settings = {
        "password_requirements": {
            "minimum_length": "8 characters",
            "required_elements": ["Uppercase letter", "Lowercase letter", "Number", "Special character"],
            "restrictions": ["Cannot contain email address", "Cannot be recently used password"]
        },
        "two_factor_authentication": {
            "availability": "Optional SMS or authenticator app",
            "setup": "Account Settings > Security > Enable 2FA",
            "backup_codes": "Download backup codes for account recovery"
        },
        "privacy_controls": {
            "data_preferences": "Control marketing communications and data usage",
            "account_deletion": "Request account deletion through customer service",
            "data_download": "Request copy of personal data"
        }
    }

    result = {"general_guidance": "Always verify customer identity before discussing account details"}

    issue_responses = {
        "login": {"troubleshooting": login_troubleshooting},
        "password": {"password_help": login_troubleshooting["forgot_password"], "requirements": security_settings["password_requirements"]},
        "registration": {"signup_process": "Step-by-step account creation guidance", "verification": login_troubleshooting["email_verification"]},
        "profile": {"management": account_management["profile_updates"]},
        "security": {"settings": security_settings},
        "orders": {"history": account_management["order_history"]}
    }

    if issue_type.lower() in issue_responses:
        result.update(issue_responses[issue_type.lower()])

    result["immediate_actions"] = {
        "login_issues": "Try password reset first",
        "account_security": "Enable two-factor authentication",
        "profile_problems": "Verify email address is current",
        "technical_issues": "Clear browser cache and cookies"
    }

    result["escalation_criteria"] = [
        "Customer suspects account compromise",
        "Technical issues persist after troubleshooting",
        "Request for account deletion or data export",
        "Unable to access account for 24+ hours"
    ]

    result["self_service_resources"] = [
        "Password reset: example.com/forgot-password",
        "Account settings: example.com/account",
        "Help center: example.com/help/account",
        "Contact form: example.com/contact"
    ]

    return result

# =============================================================================
# 8. LOYALTY & REWARDS PROGRAM
# =============================================================================

@mcp.tool()
def get_loyalty_program_info(inquiry_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get information about loyalty program, rewards, and member benefits.

    Args:
        inquiry_type: Type of inquiry (enrollment, benefits, points, tiers, etc.)
    """

    program_overview = {
        "name": "VIP Rewards Program",
        "enrollment": "Free to join, automatic with first purchase",
        "earning_rate": "1 point per $1 spent",
        "redemption_rate": "100 points = $5 reward",
        "point_expiration": "Points expire after 12 months of inactivity"
    }

    membership_tiers = {
        "bronze": {
            "requirement": "$0 - $499 annual spending",
            "benefits": ["1x points earning", "Member-only sales", "Free shipping on $75+"],
            "welcome_bonus": "100 points upon enrollment"
        },
        "silver": {
            "requirement": "$500 - $999 annual spending",
            "benefits": ["1.25x points earning", "Early sale access", "Free shipping on $50+", "Birthday reward"],
            "upgrade_bonus": "250 points when reaching Silver"
        },
        "gold": {
            "requirement": "$1000 - $2499 annual spending",
            "benefits": ["1.5x points earning", "Free shipping all orders", "Exclusive products", "Priority support"],
            "upgrade_bonus": "500 points when reaching Gold"
        },
        "platinum": {
            "requirement": "$2500+ annual spending",
            "benefits": ["2x points earning", "Free expedited shipping", "Personal shopper", "Concierge service"],
            "upgrade_bonus": "1000 points when reaching Platinum"
        }
    }

    earning_opportunities = {
        "purchases": "1 point per $1 spent (multiplied by tier bonus)",
        "reviews": "25 points per product review",
        "referrals": "500 points for each successful referral",
        "birthday": "2x points on all purchases during birthday month",
        "social_media": "50 points for social media follows/shares",
        "surveys": "10-50 points for completing customer surveys"
    }

    redemption_options = {
        "reward_certificates": {
            "values": ["$5 (100 points)", "$10 (200 points)", "$25 (500 points)", "$50 (1000 points)"],
            "usage": "Apply at checkout like a gift card",
            "expiration": "Certificates expire 90 days after issue"
        },
        "exclusive_merchandise": "Special items only available with points",
        "experiences": "Concert tickets, events, and exclusive experiences",
        "charity_donations": "Donate points to partner charities"
    }

    result = {"program_overview": program_overview}

    inquiry_responses = {
        "enrollment": {
            "process": "Automatic enrollment with first purchase or manual signup",
            "requirements": "Valid email address and phone number",
            "welcome_offer": "100 bonus points + 20% off next purchase"
        },
        "benefits": {"tiers": membership_tiers},
        "points": {
            "earning": earning_opportunities,
            "redemption": redemption_options,
            "balance_check": "View points balance in account dashboard or email receipt"
        },
        "tiers": {
            "levels": membership_tiers,
            "progression": "Tier status based on previous 12 months spending",
            "tier_updates": "Status reviewed monthly, upgrades effective immediately"
        }
    }

    if inquiry_type and inquiry_type.lower() in inquiry_responses:
        result[f"{inquiry_type.lower()}_details"] = inquiry_responses[inquiry_type.lower()]

    result["program_rules"] = [
        "Points earned on net purchase amount (after discounts)",
        "Returns result in point deduction from account",
        "One account per person/email address",
        "Points cannot be transferred between accounts",
        "Program benefits subject to change with 30-day notice"
    ]

    result["customer_service_tips"] = [
        "Check account for missing points from recent purchases",
        "Explain tier benefits clearly to encourage program engagement",
        "Remind customers about expiring points or certificates",
        "Offer enrollment if customer isn't already a member"
    ]

    result["common_questions"] = {
        "missing_points": "Points typically post within 24-48 hours of order shipment",
        "expired_points": "Expired points cannot be restored, but make exception for recent expirations",
        "tier_benefits": "Tier benefits apply immediately upon reaching spending threshold",
        "point_value": "Points are worth 5 cents each when redeemed for certificates"
    }

    return result

# =============================================================================
# 10. PRODUCT CARE & MAINTENANCE - Post-purchase support
# =============================================================================

@mcp.tool()
def get_product_care_info(product_category: str, material: Optional[str] = None) -> Dict[str, Any]:
    """
    Get care instructions and maintenance information for products.

    Args:
        product_category: Category of product (clothing, shoes, electronics, furniture, etc.)
        material: Specific material if relevant (leather, cotton, silk, etc.)
    """

    clothing_care = {
        "cotton": {
            "washing": "Machine wash cold, gentle cycle",
            "drying": "Tumble dry low or hang dry",
            "ironing": "Medium heat, steam if needed",
            "storage": "Fold or hang, avoid prolonged sun exposure",
            "stain_removal": "Pre-treat stains promptly with cold water"
        },
        "silk": {
            "washing": "Hand wash or dry clean only",
            "drying": "Lay flat on towel, away from direct sunlight",
            "ironing": "Low heat on reverse side with pressing cloth",
            "storage": "Hang on padded hangers, use garment bags",
            "special_care": "Avoid deodorants and perfumes on fabric"
        },
        "wool": {
            "washing": "Hand wash in cold water or dry clean",
            "drying": "Lay flat to dry, reshape while damp",
            "ironing": "Low heat with steam, use pressing cloth",
            "storage": "Fold with cedar blocks or lavender sachets",
            "pilling": "Use fabric shaver to remove pills gently"
        },
        "leather": {
            "cleaning": "Wipe with damp cloth, use leather cleaner monthly",
            "conditioning": "Apply leather conditioner every 3-6 months",
            "storage": "Store in breathable garment bag, use shoe trees",
            "water_damage": "Blot immediately, let air dry naturally",
            "scratches": "Minor scratches often disappear with conditioning"
        }
    }

    electronics_care = {
        "smartphones": {
            "cleaning": "Turn off device, use microfiber cloth with isopropyl alcohol",
            "charging": "Use original charger, avoid overcharging overnight",
            "storage": "Keep in protective case, avoid extreme temperatures",
            "battery_care": "Charge between 20-80% for optimal battery health",
            "water_damage": "Turn off immediately, do not charge, seek professional help"
        },
        "laptops": {
            "cleaning": "Shut down, clean keyboard with compressed air, screen with microfiber cloth",
            "ventilation": "Keep vents clear, use on hard surfaces for airflow",
            "battery": "Calibrate monthly, store at 50% charge if unused long-term",
            "updates": "Install security updates promptly, backup data regularly",
            "transport": "Use padded case, never grab by screen"
        }
    }

    furniture_care = {
        "wood": {
            "cleaning": "Dust regularly with microfiber cloth",
            "polishing": "Use wood polish monthly, follow grain direction",
            "protection": "Use coasters, placemats, and tablecloths",
            "environment": "Avoid direct sunlight and heat sources",
            "scratches": "Minor scratches can be buffed with walnut meat"
        },
        "upholstery": {
            "vacuuming": "Weekly vacuuming with upholstery attachment",
            "spot_cleaning": "Blot spills immediately, don't rub",
            "professional_cleaning": "Deep clean every 12-18 months",
            "rotation": "Rotate and flip cushions monthly for even wear",
            "protection": "Use fabric protector spray annually"
        }
    }

    result = {}

    category_care = {
        "clothing": clothing_care,
        "electronics": electronics_care,
        "furniture": furniture_care,
        "shoes": {
            "leather_shoes": clothing_care["leather"],
            "athletic_shoes": {
                "cleaning": "Remove laces, clean with soft brush and mild detergent",
                "drying": "Air dry at room temperature, use newspaper to absorb moisture",
                "rotation": "Rotate between pairs to allow 24-hour drying time",
                "storage": "Use shoe trees to maintain shape"
            }
        }
    }

    if product_category.lower() in category_care:
        category_info = category_care[product_category.lower()]

        if material and material.lower() in category_info:
            result["specific_care"] = category_info[material.lower()]
        else:
            result["care_options"] = category_info

    result["general_tips"] = [
        "Read care labels before cleaning any item",
        "Test cleaning products on inconspicuous area first",
        "Address stains and damage promptly for best results",
        "Follow manufacturer instructions over generic advice",
        "Keep receipts and documentation for warranty claims"
    ]

    result["professional_services"] = {
        "when_needed": [
            "Stubborn stains that home remedies can't remove",
            "Expensive or delicate items requiring special care",
            "Warranty repairs for electronics and appliances",
            "Restoration of antique or valuable pieces"
        ],
        "finding_services": "Check manufacturer recommendations for authorized service providers"
    }

    result["warranty_considerations"] = [
        "Improper care may void warranty",
        "Keep documentation of professional cleaning/repairs",
        "Some damage covered under product guarantees",
        "Contact customer service before attempting major repairs"
    ]

    result["customer_service_guidance"] = [
        "Ask about specific product and material for targeted advice",
        "Recommend professional cleaning for expensive items",
        "Offer replacement if damage occurred during shipping",
        "Escalate if customer claims care instructions were inadequate"
    ]

    return result

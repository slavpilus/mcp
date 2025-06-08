"""Test the new support tools in mcp_tools.py."""

from unittest.mock import Mock

import pytest

from mcp_server.mcp_tools import register_tools


@pytest.fixture
def mock_mcp_instance():
    """Create a mock FastMCP instance."""
    mock_mcp = Mock()
    # Mock the tool decorator to return the function unchanged
    mock_mcp.tool = Mock(side_effect=lambda: lambda func: func)
    return mock_mcp


@pytest.fixture
def support_tools(mock_mcp_instance):
    """Get the registered support tools."""
    return register_tools(mock_mcp_instance)


# =============================================================================
# Return Policy Tests
# =============================================================================


def test_get_return_policy_general(support_tools):
    """Test get_return_policy with no category specified."""
    result = support_tools["get_return_policy"]()

    assert "general_policy" in result
    assert result["general_policy"]["standard_return_window"] == "30 days"
    assert "condition_requirements" in result["general_policy"]
    assert "helpful_tips" in result
    assert "escalation_triggers" in result
    assert len(result["helpful_tips"]) == 4
    assert len(result["escalation_triggers"]) == 3


def test_get_return_policy_electronics(support_tools):
    """Test get_return_policy for electronics category."""
    result = support_tools["get_return_policy"]("electronics")

    assert "general_policy" in result
    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "15 days"
    assert result["category_specific"]["restocking_fee"] == "10% for opened items"
    assert "customer_service_notes" in result
    assert "electronics" in result["customer_service_notes"][0]


def test_get_return_policy_clothing(support_tools):
    """Test get_return_policy for clothing category."""
    result = support_tools["get_return_policy"]("clothing")

    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "45 days"
    assert "size_exchange" in result["category_specific"]


def test_get_return_policy_books(support_tools):
    """Test get_return_policy for books category."""
    result = support_tools["get_return_policy"]("books")

    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "30 days"
    assert "digital_content" in result["category_specific"]


def test_get_return_policy_custom_items(support_tools):
    """Test get_return_policy for custom items category."""
    result = support_tools["get_return_policy"]("custom_items")

    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "Non-returnable"
    assert "exceptions" in result["category_specific"]


def test_get_return_policy_unknown_category(support_tools):
    """Test get_return_policy with unknown category."""
    result = support_tools["get_return_policy"]("unknown")

    assert "general_policy" in result
    assert "category_specific" not in result
    assert "customer_service_notes" not in result


# =============================================================================
# Shipping Info Tests
# =============================================================================


def test_get_shipping_info_basic(support_tools):
    """Test get_shipping_info with no parameters."""
    result = support_tools["get_shipping_info"]()

    assert "domestic_options" in result
    assert "processing_time" in result
    assert "cutoff_times" in result
    assert "shipping_restrictions" in result

    # Check domestic shipping options
    domestic = result["domestic_options"]
    assert "standard_shipping" in domestic
    assert "expedited_shipping" in domestic
    assert "overnight_shipping" in domestic
    assert "free_shipping" in domestic
    assert domestic["free_shipping"]["threshold"] == 75.00


def test_get_shipping_info_with_order_value_eligible(support_tools):
    """Test get_shipping_info with order value eligible for free shipping."""
    result = support_tools["get_shipping_info"](order_value=100.0)

    assert "free_shipping_eligible" in result
    assert result["free_shipping_eligible"] is True
    assert "customer_guidance" in result
    assert "qualifies for free shipping" in result["customer_guidance"]


def test_get_shipping_info_with_order_value_not_eligible(support_tools):
    """Test get_shipping_info with order value not eligible for free shipping."""
    result = support_tools["get_shipping_info"](order_value=50.0)

    assert "free_shipping_eligible" in result
    assert result["free_shipping_eligible"] is False
    assert "customer_guidance" in result
    assert "Add $25.00 more" in result["customer_guidance"]


def test_get_shipping_info_canada(support_tools):
    """Test get_shipping_info for Canada."""
    result = support_tools["get_shipping_info"](destination_country="canada")

    assert "international_shipping" in result
    assert result["international_shipping"]["standard"] == "$15.99"
    assert result["international_shipping"]["timeframe"] == "7-14 days"
    assert "international_notes" in result


def test_get_shipping_info_uk(support_tools):
    """Test get_shipping_info for UK."""
    result = support_tools["get_shipping_info"](destination_country="UK")

    assert "international_shipping" in result
    assert result["international_shipping"]["standard"] == "$19.99"


def test_get_shipping_info_unknown_country(support_tools):
    """Test get_shipping_info for unknown country."""
    result = support_tools["get_shipping_info"](destination_country="mars")

    assert "international_shipping" in result
    assert (
        result["international_shipping"]
        == "Contact support for rates to this destination"
    )


# =============================================================================
# Contact Information Tests
# =============================================================================


def test_get_contact_information_general(support_tools):
    """Test get_contact_information with no parameters."""
    result = support_tools["get_contact_information"]()

    assert "general_contact" in result
    assert "self_service_options" in result
    assert "customer_service_tips" in result

    # Check general contact info
    contact = result["general_contact"]
    assert "phone" in contact
    assert "email" in contact
    assert "live_chat" in contact
    assert "business_hours" in contact


def test_get_contact_information_billing(support_tools):
    """Test get_contact_information for billing issues."""
    result = support_tools["get_contact_information"](issue_type="billing")

    assert "specialized_contact" in result
    assert "routing_advice" in result

    billing = result["specialized_contact"]
    assert billing["department"] == "Billing & Payments"
    assert billing["phone"] == "1-800-BILLING (1-800-245-5464)"
    assert "Billing & Payments" in result["routing_advice"]


def test_get_contact_information_technical(support_tools):
    """Test get_contact_information for technical issues."""
    result = support_tools["get_contact_information"](issue_type="technical")

    assert "specialized_contact" in result
    technical = result["specialized_contact"]
    assert technical["department"] == "Technical Support"
    assert "24/7" in technical["hours"]


def test_get_contact_information_returns(support_tools):
    """Test get_contact_information for returns."""
    result = support_tools["get_contact_information"](issue_type="returns")

    assert "specialized_contact" in result
    returns = result["specialized_contact"]
    assert returns["department"] == "Returns & Exchanges"
    assert "online_portal" in returns


def test_get_contact_information_emergency(support_tools):
    """Test get_contact_information with emergency urgency."""
    result = support_tools["get_contact_information"](urgency="emergency")

    assert "urgency_guidance" in result
    emergency = result["urgency_guidance"]
    assert emergency["recommended_contact"] == "phone"
    assert "security issues" in emergency["note"]


def test_get_contact_information_high_urgency(support_tools):
    """Test get_contact_information with high urgency."""
    result = support_tools["get_contact_information"](urgency="high")

    assert "urgency_guidance" in result
    high = result["urgency_guidance"]
    assert "phone or live_chat" in high["recommended_contact"]


def test_get_contact_information_low_urgency(support_tools):
    """Test get_contact_information with low urgency."""
    result = support_tools["get_contact_information"](urgency="low")

    assert "urgency_guidance" in result
    low = result["urgency_guidance"]
    assert low["recommended_contact"] == "email"


# =============================================================================
# Size Guide Tests
# =============================================================================


def test_get_size_guide_shirts(support_tools):
    """Test get_size_guide for shirts."""
    result = support_tools["get_size_guide"]("shirts")

    assert "measuring_instructions" in result
    assert "size_chart" in result
    assert "product_specific_notes" in result
    assert "fitting_tips" in result
    assert "exchange_policy" in result

    # Check size chart structure
    chart = result["size_chart"]
    assert "mens" in chart
    assert "womens" in chart
    assert "M" in chart["mens"]
    assert chart["mens"]["M"]["chest"] == "38-40"


def test_get_size_guide_shoes(support_tools):
    """Test get_size_guide for shoes."""
    result = support_tools["get_size_guide"]("shoes")

    assert "size_chart" in result
    chart = result["size_chart"]
    assert "mens" in chart
    assert "womens" in chart
    assert "9" in chart["mens"]
    assert chart["mens"]["9"]["us"] == "9"
    assert chart["mens"]["9"]["eu"] == "42"


def test_get_size_guide_dresses(support_tools):
    """Test get_size_guide for dresses."""
    result = support_tools["get_size_guide"]("dresses")

    assert "size_chart" in result
    chart = result["size_chart"]
    assert "sizes" in chart
    assert "M" in chart["sizes"]
    assert "Variable by style" in chart["sizes"]["M"]["length"]


def test_get_size_guide_unknown_product(support_tools):
    """Test get_size_guide for unknown product type."""
    result = support_tools["get_size_guide"]("unknown")

    assert "measuring_instructions" in result
    assert "fitting_tips" in result
    assert "exchange_policy" in result
    assert "size_chart" not in result


def test_get_size_guide_with_brand(support_tools):
    """Test get_size_guide with brand parameter."""
    result = support_tools["get_size_guide"]("shirts", brand="nike")

    # Brand parameter is accepted but not used in current implementation
    assert "measuring_instructions" in result
    assert "size_chart" in result


# =============================================================================
# Warranty Information Tests
# =============================================================================


def test_get_warranty_information_electronics(support_tools):
    """Test get_warranty_information for electronics."""
    result = support_tools["get_warranty_information"]("electronics")

    assert "warranty_terms" in result
    assert "claim_process" in result
    assert "satisfaction_guarantee" in result
    assert "customer_service_notes" in result

    warranty = result["warranty_terms"]
    assert warranty["standard_warranty"] == "1 year from purchase date"
    assert "Manufacturing defects" in warranty["coverage"]
    assert "Physical damage" in warranty["exclusions"]


def test_get_warranty_information_appliances(support_tools):
    """Test get_warranty_information for appliances."""
    result = support_tools["get_warranty_information"]("appliances")

    warranty = result["warranty_terms"]
    assert "2 years" in warranty["standard_warranty"]
    assert "Motor failures" in warranty["coverage"]


def test_get_warranty_information_furniture(support_tools):
    """Test get_warranty_information for furniture."""
    result = support_tools["get_warranty_information"]("furniture")

    warranty = result["warranty_terms"]
    assert "5 years structural" in warranty["standard_warranty"]
    assert "Frame defects" in warranty["coverage"]


def test_get_warranty_information_clothing(support_tools):
    """Test get_warranty_information for clothing."""
    result = support_tools["get_warranty_information"]("clothing")

    warranty = result["warranty_terms"]
    assert "90 days" in warranty["standard_warranty"]
    assert "Seam failures" in warranty["coverage"]


def test_get_warranty_information_with_valid_date(support_tools):
    """Test get_warranty_information with valid purchase date."""
    result = support_tools["get_warranty_information"]("electronics", "2024-01-01")

    assert "warranty_status" in result
    status = result["warranty_status"]
    assert "days_since_purchase" in status
    assert "days_remaining" in status
    assert "status" in status
    assert "expiration_date" in status


def test_get_warranty_information_with_invalid_date(support_tools):
    """Test get_warranty_information with invalid purchase date."""
    result = support_tools["get_warranty_information"]("electronics", "invalid-date")

    assert "date_error" in result
    assert "Invalid date format" in result["date_error"]


def test_get_warranty_information_unknown_category(support_tools):
    """Test get_warranty_information for unknown category."""
    result = support_tools["get_warranty_information"]("unknown")

    assert "warranty_terms" not in result
    assert "claim_process" in result
    assert "satisfaction_guarantee" in result


# =============================================================================
# Payment Information Tests
# =============================================================================


def test_get_payment_information_basic(support_tools):
    """Test get_payment_information with no parameters."""
    result = support_tools["get_payment_information"]()

    assert "accepted_payments" in result
    assert "billing_information" in result
    assert "customer_service_guidance" in result
    assert "self_service_options" in result

    payments = result["accepted_payments"]
    assert "credit_cards" in payments
    assert "digital_wallets" in payments
    assert "buy_now_pay_later" in payments


def test_get_payment_information_security(support_tools):
    """Test get_payment_information for security inquiry."""
    result = support_tools["get_payment_information"]("security")

    assert "security_details" in result
    security = result["security_details"]
    assert "fraud_protection" in security
    assert "cvv_verification" in security
    assert "pci_compliance" in security


def test_get_payment_information_issues(support_tools):
    """Test get_payment_information for issues inquiry."""
    result = support_tools["get_payment_information"]("issues")

    assert "troubleshooting" in result
    issues = result["troubleshooting"]
    assert "declined_cards" in issues
    assert "duplicate_charges" in issues
    assert "international_cards" in issues


def test_get_payment_information_methods(support_tools):
    """Test get_payment_information for methods inquiry."""
    result = support_tools["get_payment_information"]("methods")

    assert "detailed_methods" in result
    # Should be same as accepted_payments
    assert result["detailed_methods"] == result["accepted_payments"]


def test_get_payment_information_billing(support_tools):
    """Test get_payment_information for billing inquiry."""
    result = support_tools["get_payment_information"]("billing")

    assert "billing_details" in result
    # Should be same as billing_information
    assert result["billing_details"] == result["billing_information"]


# =============================================================================
# Account Help Tests
# =============================================================================


def test_get_account_help_login(support_tools):
    """Test get_account_help for login issues."""
    result = support_tools["get_account_help"]("login")

    assert "general_guidance" in result
    assert "troubleshooting" in result
    assert "immediate_actions" in result
    assert "escalation_criteria" in result
    assert "self_service_resources" in result

    troubleshooting = result["troubleshooting"]
    assert "forgot_password" in troubleshooting
    assert "account_locked" in troubleshooting
    assert "email_verification" in troubleshooting


def test_get_account_help_password(support_tools):
    """Test get_account_help for password issues."""
    result = support_tools["get_account_help"]("password")

    assert "password_help" in result
    assert "requirements" in result

    requirements = result["requirements"]
    assert "minimum_length" in requirements
    assert requirements["minimum_length"] == "8 characters"


def test_get_account_help_registration(support_tools):
    """Test get_account_help for registration issues."""
    result = support_tools["get_account_help"]("registration")

    assert "signup_process" in result
    assert "verification" in result


def test_get_account_help_profile(support_tools):
    """Test get_account_help for profile issues."""
    result = support_tools["get_account_help"]("profile")

    assert "management" in result
    management = result["management"]
    assert "editable_fields" in management
    assert "Email" in management["editable_fields"]


def test_get_account_help_security(support_tools):
    """Test get_account_help for security issues."""
    result = support_tools["get_account_help"]("security")

    assert "settings" in result
    settings = result["settings"]
    assert "password_requirements" in settings
    assert "two_factor_authentication" in settings
    assert "privacy_controls" in settings


def test_get_account_help_orders(support_tools):
    """Test get_account_help for order history issues."""
    result = support_tools["get_account_help"]("orders")

    assert "history" in result
    history = result["history"]
    assert "access" in history
    assert "actions" in history
    assert "retention" in history


def test_get_account_help_unknown_issue(support_tools):
    """Test get_account_help for unknown issue type."""
    result = support_tools["get_account_help"]("unknown")

    assert "general_guidance" in result
    assert "immediate_actions" in result
    assert "escalation_criteria" in result
    # Should not have specific issue responses
    assert "troubleshooting" not in result


# =============================================================================
# Loyalty Program Tests
# =============================================================================


def test_get_loyalty_program_info_basic(support_tools):
    """Test get_loyalty_program_info with no parameters."""
    result = support_tools["get_loyalty_program_info"]()

    assert "program_overview" in result
    assert "program_rules" in result
    assert "customer_service_tips" in result
    assert "common_questions" in result

    overview = result["program_overview"]
    assert overview["name"] == "VIP Rewards Program"
    assert overview["earning_rate"] == "1 point per $1 spent"
    assert overview["redemption_rate"] == "100 points = $5 reward"


def test_get_loyalty_program_info_enrollment(support_tools):
    """Test get_loyalty_program_info for enrollment inquiry."""
    result = support_tools["get_loyalty_program_info"]("enrollment")

    assert "enrollment_details" in result
    enrollment = result["enrollment_details"]
    assert "process" in enrollment
    assert "requirements" in enrollment
    assert "welcome_offer" in enrollment


def test_get_loyalty_program_info_benefits(support_tools):
    """Test get_loyalty_program_info for benefits inquiry."""
    result = support_tools["get_loyalty_program_info"]("benefits")

    assert "benefits_details" in result
    benefits = result["benefits_details"]
    assert "tiers" in benefits

    tiers = benefits["tiers"]
    assert "bronze" in tiers
    assert "silver" in tiers
    assert "gold" in tiers
    assert "platinum" in tiers


def test_get_loyalty_program_info_points(support_tools):
    """Test get_loyalty_program_info for points inquiry."""
    result = support_tools["get_loyalty_program_info"]("points")

    assert "points_details" in result
    points = result["points_details"]
    assert "earning" in points
    assert "redemption" in points
    assert "balance_check" in points


def test_get_loyalty_program_info_tiers(support_tools):
    """Test get_loyalty_program_info for tiers inquiry."""
    result = support_tools["get_loyalty_program_info"]("tiers")

    assert "tiers_details" in result
    tiers = result["tiers_details"]
    assert "levels" in tiers
    assert "progression" in tiers
    assert "tier_updates" in tiers


# =============================================================================
# Product Care Tests
# =============================================================================


def test_get_product_care_info_clothing_cotton(support_tools):
    """Test get_product_care_info for clothing with cotton material."""
    result = support_tools["get_product_care_info"]("clothing", "cotton")

    assert "specific_care" in result
    assert "general_tips" in result
    assert "professional_services" in result
    assert "warranty_considerations" in result
    assert "customer_service_guidance" in result

    care = result["specific_care"]
    assert "washing" in care
    assert "drying" in care
    assert care["washing"] == "Machine wash cold, gentle cycle"


def test_get_product_care_info_clothing_silk(support_tools):
    """Test get_product_care_info for clothing with silk material."""
    result = support_tools["get_product_care_info"]("clothing", "silk")

    care = result["specific_care"]
    assert "Hand wash or dry clean only" in care["washing"]
    assert "special_care" in care


def test_get_product_care_info_clothing_leather(support_tools):
    """Test get_product_care_info for clothing with leather material."""
    result = support_tools["get_product_care_info"]("clothing", "leather")

    care = result["specific_care"]
    assert "conditioning" in care
    assert "water_damage" in care


def test_get_product_care_info_electronics_no_material(support_tools):
    """Test get_product_care_info for electronics without specific material."""
    result = support_tools["get_product_care_info"]("electronics")

    assert "care_options" in result
    assert "specific_care" not in result

    options = result["care_options"]
    assert "smartphones" in options
    assert "laptops" in options


def test_get_product_care_info_furniture(support_tools):
    """Test get_product_care_info for furniture."""
    result = support_tools["get_product_care_info"]("furniture")

    assert "care_options" in result
    options = result["care_options"]
    assert "wood" in options
    assert "upholstery" in options


def test_get_product_care_info_shoes(support_tools):
    """Test get_product_care_info for shoes."""
    result = support_tools["get_product_care_info"]("shoes")

    assert "care_options" in result
    options = result["care_options"]
    assert "leather_shoes" in options
    assert "athletic_shoes" in options


def test_get_product_care_info_unknown_category(support_tools):
    """Test get_product_care_info for unknown category."""
    result = support_tools["get_product_care_info"]("unknown")

    assert "care_options" not in result
    assert "specific_care" not in result
    assert "general_tips" in result
    assert "professional_services" in result


def test_get_product_care_info_unknown_material(support_tools):
    """Test get_product_care_info for known category with unknown material."""
    result = support_tools["get_product_care_info"]("clothing", "unknown")

    assert "care_options" in result
    assert "specific_care" not in result
    # Should return all clothing care options
    options = result["care_options"]
    assert "cotton" in options
    assert "silk" in options


# =============================================================================
# Integration Tests
# =============================================================================


def test_all_tools_registered(support_tools):
    """Test that all support tools are properly registered."""
    expected_tools = {
        "get_order_status",
        "cancel_order",
        "process_return",
        "track_package",
        "get_support_info",
        "get_return_policy",
        "get_shipping_info",
        "get_contact_information",
        "get_size_guide",
        "get_warranty_information",
        "get_payment_information",
        "get_account_help",
        "get_loyalty_program_info",
        "get_product_care_info",
    }

    assert set(support_tools.keys()) == expected_tools

    # Check that all tools are callable
    for tool_name, tool_func in support_tools.items():
        assert callable(tool_func), f"{tool_name} should be callable"


def test_tool_decorators_called(mock_mcp_instance):
    """Test that mcp.tool() decorator is called for each tool."""
    register_tools(mock_mcp_instance)

    # Should be called 14 times (5 original + 9 new tools)
    assert mock_mcp_instance.tool.call_count == 14


def test_tool_return_types(support_tools):
    """Test that all new support tools return dictionaries."""
    # Test non-async tools (new support tools)
    dict_tools = [
        "get_return_policy",
        "get_shipping_info",
        "get_contact_information",
        "get_size_guide",
        "get_warranty_information",
        "get_payment_information",
        "get_account_help",
        "get_loyalty_program_info",
        "get_product_care_info",
    ]

    for tool_name in dict_tools:
        tool = support_tools[tool_name]
        # Call with minimal required parameters
        if tool_name == "get_size_guide":
            result = tool("shirts")
        elif tool_name == "get_warranty_information":
            result = tool("electronics")
        elif tool_name == "get_account_help":
            result = tool("login")
        elif tool_name == "get_product_care_info":
            result = tool("clothing")
        else:
            result = tool()

        assert isinstance(result, dict), f"{tool_name} should return a dict"
        assert len(result) > 0, f"{tool_name} should return non-empty dict"

"""
Demo/offline LLM that provides canned responses for demonstration.
Used when no real API key is available.
"""
from typing import Any, List, Optional, Dict
from langchain.chat_models.base import BaseChatModel, SimpleChatModel
from langchain.schema import AIMessage, BaseMessage, ChatResult, ChatGeneration
from langchain.callbacks.manager import CallbackManagerForLLMRun
from core.logging_utils import get_logger

logger = get_logger(__name__)


class DemoLLM(SimpleChatModel):
    """
    Demo LLM that provides realistic canned responses based on context.
    """
    
    model_name: str = "demo-llm"
    
    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response based on the input messages.
        """
        # Get the last user message
        user_message = ""
        context_docs = ""
        
        for msg in messages:
            content = msg.content
            if isinstance(content, str):
                if "Context:" in content or "context:" in content:
                    # Extract context
                    context_docs = content
                else:
                    user_message = content
        
        # Generate response based on question keywords
        response = self._generate_response(user_message, context_docs)
        
        return response
    
    def _generate_response(self, question: str, context: str) -> str:
        """
        Generate a contextual response based on the question and context.
        """
        question_lower = question.lower()
        
        # Check what type of question this is
        if any(word in question_lower for word in ["vacation", "pto", "time off", "leave"]):
            return self._vacation_response(context)
        elif any(word in question_lower for word in ["sales", "revenue", "q4", "quarter"]):
            return self._sales_response(context)
        elif any(word in question_lower for word in ["lease", "rent", "tenant", "landlord"]):
            return self._lease_response(context)
        elif any(word in question_lower for word in ["risk", "obligation", "compliance", "legal"]):
            return self._risk_response(context)
        elif any(word in question_lower for word in ["employee", "staff", "hr", "handbook"]):
            return self._employee_response(context)
        else:
            return self._generic_response(context)
    
    def _vacation_response(self, context: str) -> str:
        return """Based on the employee handbook, the vacation policy includes:

1. **Paid Time Off (PTO)**: Employees accrue PTO based on tenure:
   - 0-2 years: 10 days per year
   - 3-5 years: 15 days per year
   - 6+ years: 20 days per year

2. **Rollover**: Up to 5 unused PTO days can roll over to the next year

3. **Approval Process**: Vacation requests must be submitted at least 2 weeks in advance and approved by the direct manager

4. **Holidays**: In addition to PTO, employees receive 10 paid holidays per year

The policy aims to promote work-life balance while ensuring adequate staffing coverage."""
    
    def _sales_response(self, context: str) -> str:
        return """Based on the Q4 sales data, here are the key highlights:

1. **Total Revenue**: $2.4M for Q4, representing a 15% increase over Q3

2. **Top Performing Regions**:
   - North America: $1.2M (50% of total)
   - Europe: $750K (31%)
   - Asia-Pacific: $450K (19%)

3. **Product Performance**:
   - Premium tier products showed strongest growth at 25% QoQ
   - Standard tier maintained steady performance

4. **Growth Drivers**:
   - New customer acquisitions up 20%
   - Existing customer expansion contributed 40% of revenue growth
   - Successful launch of two new product features

Q4 exceeded targets by 8%, positioning us well for year-end goals."""
    
    def _lease_response(self, context: str) -> str:
        return """Based on the lease agreement, key terms include:

1. **Lease Duration**: 12-month term with option to renew for an additional 12 months

2. **Monthly Rent**: $2,500 due on the 1st of each month

3. **Security Deposit**: $5,000 (equivalent to 2 months rent)

4. **Maintenance Responsibilities**:
   - Landlord: Major repairs, structural issues, HVAC maintenance
   - Tenant: Minor repairs, routine maintenance, utilities

5. **Termination**: 60-day notice required for non-renewal

6. **Restrictions**: No subletting without written consent, no pets over 25 lbs

The agreement follows standard commercial lease practices and includes standard liability and insurance clauses."""
    
    def _risk_response(self, context: str) -> str:
        return """Based on the uploaded documents, key risks and obligations include:

**Legal & Compliance Risks:**
- Lease agreement requires maintaining proper insurance coverage
- Non-compliance with notice periods could result in penalties
- Property damage beyond normal wear-and-tear is tenant's responsibility

**HR & Employment Obligations:**
- Must maintain accurate PTO tracking and payroll records
- Equal opportunity employment policies must be followed
- Regular policy reviews and employee acknowledgments required

**Financial Obligations:**
- Timely rent payments to avoid default
- Security deposit subject to deductions for damages
- Sales revenue targets tied to performance bonuses

**Mitigation Strategies:**
- Maintain comprehensive insurance policies
- Regular policy training for managers
- Document all transactions and approvals
- Schedule regular property inspections

These obligations should be reviewed quarterly to ensure ongoing compliance."""
    
    def _employee_response(self, context: str) -> str:
        return """Based on the employee handbook, important information includes:

**Employment Policies:**
- At-will employment with equal opportunity provisions
- Standard work hours: 9 AM - 5 PM, Monday-Friday
- Remote work available with manager approval

**Benefits:**
- Health insurance (medical, dental, vision)
- 401(k) with 4% company match
- Life insurance and disability coverage
- Professional development budget: $1,500/year

**Code of Conduct:**
- Professional behavior and dress code expected
- Confidentiality and data security protocols
- Anti-harassment and discrimination policies

**Leave Policies:**
- PTO as described in vacation policy
- Sick leave: 5 days per year
- Parental leave: 12 weeks paid
- Bereavement leave: 3-5 days depending on relation

All policies are subject to annual review and updates."""
    
    def _generic_response(self, context: str) -> str:
        if not context or len(context) < 50:
            return """I apologize, but I don't have enough relevant information in the uploaded documents to provide a comprehensive answer to your question. 

The documents currently indexed include:
- Employee handbook (HR policies)
- Q4 sales data (revenue and performance metrics)
- Lease agreement (commercial property terms)

Please try rephrasing your question or asking about topics covered in these documents."""
        
        return """Based on the available documents, here's what I found:

The uploaded documents contain information about company policies, sales performance, and contractual obligations. The content includes:

- **HR Policies**: Employee benefits, time-off policies, code of conduct
- **Financial Data**: Quarterly sales figures, revenue breakdowns by region
- **Legal Agreements**: Lease terms, responsibilities, and obligations

For more specific information, please ask about:
- Vacation and PTO policies
- Sales performance and metrics
- Lease terms and conditions
- Employee benefits and policies

I'm here to help you find specific information from these documents."""
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "demo"


class ResilientChatModel(SimpleChatModel):
    """
    Chat model wrapper that tries real API first, falls back to demo mode.
    
    Note: Once fallback is activated, it remains in demo mode for the session.
    This ensures consistent demo behavior without API retry overhead.
    """
    
    model_name: str = "resilient-chat"
    _primary: Optional[BaseChatModel] = None
    _fallback: Optional[DemoLLM] = None
    _using_fallback: bool = False
    
    def __init__(self, primary: BaseChatModel, **kwargs):
        super().__init__(**kwargs)
        self._primary = primary
        self._fallback = DemoLLM()
        self._using_fallback = False
        logger.info("Initialized resilient chat model with demo fallback")
    
    def _call(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate with fallback support.
        """
        # If already using fallback, skip trying primary
        if self._using_fallback:
            return self._fallback._call(messages, stop, run_manager, **kwargs)
        
        try:
            # Try to call primary - need to convert to proper format
            if hasattr(self._primary, '_call'):
                return self._primary._call(messages, stop, run_manager, **kwargs)
            elif hasattr(self._primary, '_generate'):
                result = self._primary._generate(messages, stop, run_manager, **kwargs)
                return result.generations[0].message.content
            else:
                # Fallback to invoke
                result = self._primary.invoke(messages)
                return result.content if hasattr(result, 'content') else str(result)
        except Exception as e:
            error_str = str(e).lower()
            # Check if it's an API key, auth, or network error
            if any(keyword in error_str for keyword in [
                'api key',
                'api_key',
                'authentication',
                'unauthorized',
                '401',
                'connection',
                'network',
                'timeout',
                'failed to resolve',
                'dns',
                'connection error',
                'name resolution'
            ]):
                logger.warning(
                    f"Primary chat model failed (API/network issue), "
                    f"using demo fallback for offline demonstration. Error: {type(e).__name__}"
                )
                self._using_fallback = True
                return self._fallback._call(messages, stop, run_manager, **kwargs)
            else:
                # Re-raise if it's not an auth/network error
                raise
    
    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        if self._using_fallback:
            return "demo"
        return self._primary._llm_type if self._primary else "resilient"

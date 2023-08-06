import json
import logging
from typing import List, Tuple, cast

from fhir.resources.address import Address
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.claim import ClaimDiagnosis, ClaimInsurance, Claim, ClaimItem, ClaimCareTeam
from fhir.resources.coding import Coding
from fhir.resources.coverage import Coverage
from fhir.resources.fhirtypes import DateTime
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
from fhir.resources.organization import Organization
from fhir.resources.patient import Patient
from fhir.resources.period import Period
from fhir.resources.practitioner import Practitioner
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.relatedperson import RelatedPerson
from fhir.resources.resource import Resource

from schema.insight_engine_response import Insight, InsightType


def insight(tpe: InsightType, description: str) -> Insight:
    res = Insight()
    res.type = tpe
    res.description = description
    return res


def insight_claim_line_valid(s: str) -> Insight:
    return insight(InsightType.ClaimLineValid, s)


def insight_payable(s: str) -> Insight:
    return insight_claim_line_valid(s)


def insight_deny_claim(s: str) -> Insight:
    return insight(InsightType.ClaimNotPayable, s)


def insight_deny_claim_line(s: str) -> Insight:
    return insight(InsightType.ClaimLineNotPayable, s)


def insight_recode(s: str) -> Insight:
    return insight(InsightType.RecodeClaimLine, s)


def insight_not_applicable(s: str) -> Insight:
    return insight(InsightType.NotApplicable, s)


def insight_manual_review(s: str) -> Insight:
    return insight(InsightType.ManualReview, s)


def insight_error(s: str) -> Insight:
    return insight(InsightType.Error, s)


def _codeableconcept(code: str, system: str = None,
                     description: str = None, display: str = None) -> CodeableConcept:
    cc = CodeableConcept()
    coding = Coding()
    coding.code = code
    coding.system = system
    coding.display = display
    cc.coding = list()
    cc.coding.append(coding)
    cc.text = description
    return cc


def _name(lastname: str, firstname: str) -> HumanName:
    name = {
        "family": lastname,
        "given": [firstname]
    }
    return HumanName(**name)


def _identifier(value: str, system: str = None, tpe: str = None) -> Identifier:
    id = Identifier()
    id.system = system
    id.value = value
    if tpe:
        id.type = _codeableconcept(code=tpe)
    return id


def _address(street1: str,  city: str, state: str, postal_code: str,
             street2: str = None) -> Address:
    address = Address.construct()
    address.line = [s for s in [street1, street2] if s is not None]
    address.city = city
    address.state = state
    address.postalCode = postal_code
    return address


def program_code(pc: str) -> CodeableConcept:
    system = "https://www.hl7.org/fhir/codesystem-ex-program-code.html"
    return _codeableconcept(pc, system)


def modifier(m: str) -> CodeableConcept:
    system = "http://terminology.hl7.org/CodeSystem/modifiers"
    description = m
    return _codeableconcept(m, system, description)


def diagnosis(diag: str) -> ClaimDiagnosis:
    system = "http://terminology.hl7.org/CodeSystem/diagnoses"
    concept = _codeableconcept(diag, system)
    d = ClaimDiagnosis(**{
        "sequence": 1,
        "diagnosisCodeableConcept": concept
    })
    return d


def location(code: str, description: str = None) -> CodeableConcept:
    system = "https://www.cms.gov/medicare/coding/place-of-service-codes/place_of_service_code_set.html"
    d = _codeableconcept(code, system, description)
    return d


def service(code: str) -> CodeableConcept:
    system = "http://hl7.org/fhir/ex-serviceproduct"
    d = _codeableconcept(code, system)
    return d


def fhirdate(year: int, month: int, day: int) -> DateTime:
    return DateTime.validate(DateTime(year, month, day))


def period(start: DateTime, end: DateTime) -> Period:
    p = Period()
    p.start = start
    p.end = end
    return p


def sunits(i: int) -> Quantity:
    q = Quantity()
    q.value = i
    return q


def dunits(f: float) -> Quantity:
    q = Quantity()
    q.value = f
    return q


def claim_type(claimtype: str) -> CodeableConcept:
    system = "http://hl7.org/fhir/ValueSet/claim-type"
    d = _codeableconcept(claimtype, system)
    return d


def org_type(orgtype: str) -> CodeableConcept:
    system = "http://hl7.org/fhir/ValueSet/organization-type"
    d = _codeableconcept(orgtype, system)
    return d


def claim_num(value: str) -> List[Identifier]:
    system = "http://happydocs.com/claim"
    d = _identifier(value, system)
    return [d]


def place_of_service(code: str, display: str = None) -> CodeableConcept:
    system = "https://www.cms.gov/medicare/coding/place-of-service-codes/place_of_service_code_set.html"
    d = _codeableconcept(code=code, system=system, display=display)
    return d


def reference(value: str) -> Reference:
    ref = {
        "resource_type": "Reference",
        "reference": value
    }
    return Reference(**ref)


# modify the function and add more parameters if needed, check the code
# of the Organization class for details
def organization(name: str, _id: str = "organization-1") -> Organization:
    org = Organization()
    org.id = _id
    org.name = name
    return org


def coverage(tpe: str, order: int = None, status: str = "active",
             id: str = "coverage-1", relationship: str = "None",
             sid: str = None, patientid: str = "patient-1", orgid: str = "organization-1") -> Coverage:
    c = Coverage.construct()
    c.status = status  # status is essential for validation
    c.id = id
    c.type = _codeableconcept(tpe, system="http://terminology.hl7.org/CodeSystem/v3-ActCode")
    c.order = order
    c.subscriberId = sid
    c.relationship = _codeableconcept(relationship)
    c.beneficiary = reference(patientid)   # beneficiary is necessary for validation
    c.payor = list()  # payor is necessary for validation
    c.payor.append(reference(orgid))
    return c


def coverage_class(cov: Coverage,
                   code: str, value: str,
                   name: str) -> Coverage:
    """
    It will create a new coverage class and
    append in an existing one
    .
    :param cov:
    :param code: It should be "group", "plan" or "subplan"
    :param value:
    :param name:
    :return: Coverage
    """
    group = {
        "type":
            _codeableconcept(
                code,
                system="http://terminology.hl7.org/CodeSystem/coverage-class"
            ),
        "value": value,
        "name": name
    }
    if cov.class_fhir is None:
        cov.class_fhir = [group]
    elif isinstance(cov.class_fhir, list):
        cov.class_fhir.append(group)
    return cov


def _add_object(claim: Claim, obj: Resource):
    if not getattr(claim, "contained"):
        claim.contained = [obj]
    elif not isinstance(claim.contained, list):
        claim.contained = [obj]
    else:
        claim.contained.append(obj)


def add_coverage(cov: Coverage, claim: Claim) -> Claim:
    """
    To add the coverage object in contained list and link
    the id as reference to claim.insurance.coverage
    :param cov: Constructed Coverage Object
    to be added
    :param claim: Claim Object where Coverage needs
    to be added
    :return: Claim Object
    """
    _add_object(claim, cov)
    ins = insurance(cov, 1, True)
    if not isinstance(claim.insurance, list):
        claim.insurance = [ins]
    else:
        claim.insurance.append(ins)
    return claim


def patient(last: str, first: str,  street1: str, city: str, state: str,
            postal_code: str, _id: str = "patient-1",street2: str = None) -> Patient:
    name = _name(last, first)
    address = _address(street1, city, state, postal_code, street2)

    p = Patient.construct()
    p.id = _id

    p.name = list()
    p.name.append(name)

    p.address = list()
    p.address.append(address)
    return p


def add_patient(pat: Patient, claim: Claim) -> Claim:
    """
    To add the patient object in contained list and
    link the id as reference to claim.patient
    :param pat: contructed patient object
    to be added
    :param claim: Claim Object where
    Patient need to be added
    :return: Claim Object
    """
    _add_object(claim, pat)
    claim.patient = reference(pat.id)
    return claim


def related_person(last: str, first: str, street1: str,
                state: str, postal_code: str, city: str, street2: str = None,
                _id: str = "related-person-1", patientid: str = "patient-1") -> RelatedPerson:
    name = _name(last, first)
    address = _address(street1, city, state, postal_code, street2)

    rel = RelatedPerson.construct()
    rel.id = _id

    rel.name = list()
    rel.name.append(name)

    rel.address = list()
    rel.address.append(address)

    rel.patient = reference(patientid)
    return rel


def add_related_person(rel_person: RelatedPerson
                       , cov: Coverage
                       , claim: Claim) -> \
        Tuple[Claim, Coverage]:
    """
    To add the related person object in contained
    list and link the id as reference to
    coverage.subscriber
    :param rel_person: constructed
    related person object
    :param cov: constructed
    covergae object where reference
    to related person need to added
    :param claim: constructed
    related person object is added
    to claim.contained
    :return:Claim and Coverage Object
    """
    _add_object(claim, rel_person)
    cov.subscriber = reference(rel_person.id)
    return claim, cov


def practitioner(provtaxid: str, _id: str = "practitioner-1", tpe: str = None
                 ) -> Practitioner:
    p = Practitioner.construct()
    identifier = _identifier(value=provtaxid,
                             system="http://www.acme.org/practitioners",
                             tpe=tpe)
    p.identifier = list()
    p.identifier.append(identifier)
    p.id = _id
    return p


def add_practitioner(prc: Practitioner
                     , claim: Claim) -> Claim:
    """
    To add the practitioner object in contained
    list and link the id as reference to
    claim.provider
    This is at claim level only.
    :param prc: Constructed practitioner object
    :param claim: constructed
    practitioner object to be added
    to claim.contained
    :return: Claim Object
    """
    _add_object(claim, prc)
    claim.provider = reference(prc.id)
    return claim


def add_claim_practitioner(prc: Practitioner
                          , claim: Claim
                          , claim_line: ClaimItem) -> Tuple[Claim, ClaimItem]:
    """
    To add the practitioner object in
    list claim.item.careTeamSequence
    and link the id as reference to
    claim.careTeam.provider
    This is at claim line level only.
    :param prc:
    :param claim:
    :param claim_line:
    :return:
    """
    if not isinstance(claim.careTeam, list):
        claim.careTeam = list()
    seq = max([prov.sequence for prov in claim.careTeam], default=0) + 1
    cct = ClaimCareTeam.construct(sequence=seq)
    cct.provider = reference(prc.id)
    claim.careTeam.append(cct)
    claim_line.careTeamSequence = [seq]

    return claim, claim_line


def add_rend_prov(
        claim: Claim, claim_line: ClaimItem, prct_values: List[str],
        tpe: str = None, remove_older_prcts: bool = False
) -> Tuple[Claim, ClaimItem]:
    """
    To add rendProvNPI / rendProvTaxonomy and others to the claim. The function
    removes all Practitioner objects that are in the contained and adds
    reference for each created Practitioner object, then the first Practitioner
     object added is referenced as provider

    :param claim: the claim to add rendProvNPI to
    :param claim_line: the claim line to add rendProvNPI to
    :param prct_values: a list of practitioner values to add to the claim
    :param tpe: the type of rendProv (i.e. "TAX" if rendProvTaxonomy, "NPI"
    if rendProvNPI)
    :param remove_older_prcts: if we need to remove previous practitioners or
    not
    :return claim: the updated claim
    :return claim_item: the updated claim line
    """
    if not claim.careTeam:
        claim.careTeam = []
    add_to_seq = 0

    if remove_older_prcts:
        # removing all practitioners from contained
        for i, contained_thing in enumerate(claim.contained):
            if isinstance(contained_thing, Practitioner):
                claim.contained.pop(i)
        claim_line.careTeamSequence = []
        claim.careTeam = []
        add_to_seq2 = 0

    else:
        # leaving out the old practitioners
        add_to_seq = max([prov.sequence for prov in claim.careTeam], default=0)
        if not claim_line.careTeamSequence:
            claim_line.careTeamSequence = []
        else:
            add_to_seq2 = len(claim_line.careTeamSequence)

    # adding current practitioners
    for i, prct_value in enumerate(prct_values):
        if tpe is not None:
            prct = practitioner(
                provtaxid=prct_value, _id=f"practitioner-{add_to_seq + i + 1}",
                tpe=tpe
            )
        else:
            prct = practitioner(
                provtaxid=prct_value, _id=f"practitioner-{add_to_seq + i + 1}"
            )
        logging.warning(f"prct.id: {prct.id}")
        claim.careTeam.append(
            ClaimCareTeam(
                provider=reference(prct.id), sequence=(add_to_seq + i + 1)
            )
        )
        claim.contained.append(prct)

        claim_line.careTeamSequence.append(add_to_seq2 + i + 1)

    # referencing the first Practitioner object as provider
    claim.provider = reference("practitioner-1")

    return claim, claim_line


def insurance(ins_coverage: Coverage, seq: int, f: bool) -> ClaimInsurance:
    return ClaimInsurance(sequence=seq, focal=f, coverage=reference(ins_coverage.id))

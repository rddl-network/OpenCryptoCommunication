import ipld

ipld_ref = {
    "VersionControl": {
        "PASStandardVersionNumber": "PAS19668:2020",
        "SecurityTokenFileVersionNumber": "1.0.0"
    },
    "SecurityTokenDataStore": "https://linktoyoursecuritytokenwebsite.com/pasdata/current_version.json",
    "SecurityTokenLocation": {
        "STBlockchain": [
            {
                "STBlockchainName": "Liquid",
                "STBlockchainInformation": "https://blockstream.com/liquid/",
                "STTokenizationSolution": [
                    "RDDL Asset Registry - TMP"
                ],
                "STBlockchainUniqueAssetIdentifier": "a28d04f3e243a9a187f4a8b797be2f19a9c01b6ef4e1d65bfb6abbd6a2042097",
                "ProgrammationOfSecurityToken": "ProgramCryptoConditions",
                "SecurityTokenTransferVerificationLogic": "VerificationPreTransfer",
                "SecurityProcedures": [
                    "CapableFreezeAccount",
                    "CapableFreezeST"
                ]
            }
        ],
        "STIdentificationNumber": "Asset identification according to BS ISO 6166"
    },
    "SecurityTokenClassification": {
        "IdentificationOfST": {
            "CFICodeVersion": "1.0",
            "CFICodeValue": "CFI001"
        }
    },
    "InformationDisclosures": {
        "IssuerDisclosures": {
            "IssuerName": "TOFU International Ltd.",
            "IssuerIndustryClassification": "604885180106232618",
            "IssuerJurisdiction": "PT",
            "IssuerContactDetails": "Gilberto Tofao, 23 Rua do Murao, Nazare",
            "IssuerNewsFeed": [
                "https://tofucoin.pt/newsfeed.xss"
            ],
            "IssuerIncorporationDocuments": "https://tofucoin.pt/incorporation.doc",
            "IssuerOfferingDocuments": "https://tofucoin.pt/offering.doc",
            "IssuerAccountInformation": "https://tofucoin.pt/accounting.doc"
        },
        "IssuerAssetDisclosures": {
            "STTotalSupply": 21000000,
            "STFractionalization": True,
            "STAssetInvestmentProfile": "https://tofucoin.pt/InvestmentProfile",
            "STMarkets": [
                "https://mytofutokenexchange.com"
            ],
            "STPriceDetermination": "STMarketPrice",
            "AssetBacking": "AssetBacked",
            "AssetCustodianship": "AssetCustodied",
            "AssetCustodian": "RDDL Portugal"
        }
    },
    "EligibleInvestorClassification": {
        "EligibleInvestorCountriesList": [],
        "RestrictedCountries": [
            "PT"
        ]
    },
    "SecurityTokenTechnicalProperties": {
        "IncomeProperties": "IncomeDifferentAddress",
        "VotingProperties": "NoVoting",
        "DelegateRegister": "DelegateTA"
    },
    "KYCAMLRequirements": {
        "IdentityDocuments": "Passport",
        "ComplianceRequirements": ""
    }
}

marshalled = ipld.marshal(ipld_ref)

m_hash = ipld.multihash(marshalled)

print(m_hash)

did = { "@context" : 
{ "/" : m_hash },
  "authentication": {
    "publicKey": [
      "did:ipid:m_hash"
    ],
    "type": "EdDsaSASignatureAuthentication2022"
  },
  "created": "2022-17-09T03:00:00Z",
  "id": "did:ipid:m_hash",
  "previous": {
    "/": "zdpuAqiExr6k4AbWF6BuGkgUbVMZ7jbJyNvRz9z9yyRBxosPi"
  },
  "proof": {
    "/": "z43AaGF42R2DXsU65bNnHRCypLPr9sg6D7CUws5raiqATVaB1jj"
  },
  "publicKey": [
    {
      "curve": "ed25519",
      "expires": "2022-17-09T03:00:00Z",
      "publicKeyBase64": "qmz7tpLNKKKdl7cD7PbejDiBVp7ONpmZbfmc7cEK9mg=",
      "type": "EdDsaPublicKey"
    }
  ],
  "updated": "2022-17-09T03:01:02Z"
}

print(did)

verifiable_condition = {
     "@context": [
         "https://www.w3.org/ns/did/v1",
         "https://rddl.io/did/verifiable-conditions/v1",
         {"/" : m_hash}
     ],
    "id": F"did:example:{m_hash}",
    "type": "VerifiableCondition2021",
    "verificationMethod": [
        {
            "id": F"did:example:{m_hash}#1",
            "controller": F"did:example:{m_hash}",
            "type": "VerifiableCondition2022",
            "conditionAnd": [{
                "id": F"did:example:{m_hash}#1-1",
                "controller": F"did:example:{m_hash}",
                "type": "VerifiableCondition2021",
                "conditionOr": [{
                    "id": "did:example:{m_hash}#1-1-1",
                    "controller": F"did:example:{m_hash}",
                    "type": "ZenroomVerification2022",
                    "publicKeyBase58": "5JBxKqYKzzoHrzeqwp6zXk8wZU3Ah94ChWAinSj1fYmyJvJS5rT"
                }, {
                    "id": F"did:example:{m_hash}#1-1-2",
                    "controller": F"did:example:{m_hash}",
                    "type": "Ed25519VerificationKey2022",
                    "publicKeyBase58": "PZ8Tyr4Nx8MHsRAGMpZmZ6TWY63dXWSCzamP7YTHkZc78MJgqWsAy"
                }]
            }, {
                "id": F"did:example:{m_hash}#1-2",
                "controller": F"did:example:{m_hash}",
                "type": "Ed25519VerificationKey2022",
                "publicKeyBase58": "H3C2AVvLMv6gmMNam3uVAjZpfkcJCwDwnZn6z3wXmqPV"
            }]
        }
    ]
}

print(verifyable_condition)
import ipld
from planetmint_driver import Planetmint
from planetmint_driver.crypto import generate_keypair

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

did = {'data': { "@context" : 
{ "/" : m_hash },
  "authentication": {
    "publicKey": [
      F"did:ipid:{m_hash}"
    ],
    "type": "EdDsaSASignatureAuthentication2022"
  },
  "created": "2022-17-09T03:00:00Z",
  "id": F"did:ipid:{m_hash}",
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
}


plntmnt = Planetmint('https://test.ipdb.io')
alice = generate_keypair()
tx = plntmnt.transactions.prepare(
    operation='CREATE',
    signers=alice.public_key,
    asset=did)
signed_tx = plntmnt.transactions.fulfill(
    tx,
    private_keys=alice.private_key)
resp = plntmnt.transactions.send_commit(signed_tx)
print(resp)
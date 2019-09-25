functions = """

function MM(km, Vmax, S)
    Vmax * S / (km + S)
end

function MMWithKcat(km, kcat, S, E)
    kcat * E * S / (km + S)
end

function NonCompetitiveInhibition(km, ki, Vmax, n, I, S)
    Vmax * S / ( (km + S) * (1 + (I / ki)^n ) )
end

function NonCompetitiveInhibitionWithKcat(km, ki, kcat, E, n, I, S)
    kcat * E * S / ( (km + S) * (1 + (I / ki)^n ) )
end

function NonCompetitiveInhibitionWithKcatAndExtraActivator(km, ki, kcat, E1, E2, n, I, S)
    kcat * E1 * E2 * S / ( (km + S) * (1 + (I / ki)^n ) )
end


function MA1(k, S)
    k * S
end

function MA2(k, S1, S2)
    k * S1 * S2
end

function MA1Mod(k, S, M)
    k * S * M
end

function MA2Mod(k, S1, S2, M)
    k * S1 * S2 * M
end

function CompetitiveInhibitionWithKcat(km, ki, kcat, E, I, S)
    kcat * E * S / (km + S + ((km * I )/ ki)  )
end    

function CompetitiveInhibition(Vmax, km, ki, I, S)
    Vmax * S / (km + S + ((km * I )/ ki)  )
end

function Hill(km, kcat, E, S, h)
    kcat * E * (S / km)^h  /   (1 + (S / km)^h )
end

"""

model_string = f"""
{functions}
model ComplexPI3KModel
    compartment Cell=1;
    var IRS1 in Cell;
    var IRS1a in Cell;
    var pIRS1 in Cell;
    var PI3K in Cell;
    var pPI3K in Cell;
    var PTEN in Cell;
    var PIP2 in Cell;
    var PIP3 in Cell;
    var PDK1 in Cell;
    var PDK1_PIP3 in Cell;
    var PDK1_PIP3 in Cell;
    var Akt in Cell;
    var Akt_PIP3 in Cell;
    var pAkt in Cell;
    var Akti in Cell;
    var TSC2 in Cell;
    var pTSC2 in Cell;
    var TSC2_Rag in Cell;  
    var RagGDP in Cell;
    var RagGTP in Cell;
    var RhebGDP in Cell;
    var RhebGTP in Cell;
    var mTORC1cyt in Cell;
    var mTORC1cyt in Cell;
    var mTORC1lys in Cell;
    var mTORC1i in Cell;
    var mTORC1ii in Cell;
    var mTORC1iii in Cell;
    var FourEBP1 in Cell;
    var pFourEBP1 in Cell;
    var S6K in Cell;
    var pS6K in Cell;
    var AMPK in Cell;
    var PKC in Cell;
    var pAMPKi in Cell;
    var pAMPK in Cell;
    var CaMKK2a in Cell;
    var CaMKK2 in Cell;
    var LKB1a in Cell;
    var LKB1 in Cell;
    var RTK in Cell;
    var pRTK in Cell;
    var Sos in Cell;
    var pRTKa in Cell;
    var Raf in Cell;
    var pRaf in Cell;
    var Mek in Cell;
    var pMek in Cell;
    var Erk in Cell;
    var pErk in Cell;
    var Meki in Cell;
    var PLCeps in Cell;
    var pPLCeps in Cell;
    var IP3 in Cell;
    var DAG in Cell;
    var IpR in Cell;
    var IpRa in Cell;
    var Ca2 in Cell;
    var DUSPmRNA in Cell;
    var DUSP in Cell;

    const Insulin;
    const AA;
    const Rapamycin;
    const MK2206;
    const AZD;
    const EGF;
    const Wortmannin;
    const PMA;


    kIRS1In                 = 1;                
    kIRS1Out                = 0.1;                    
    kIRS1Act                = 0.1;                    
    kIRS1Inact              = 0.1;                    
    kIRS1Phos               = 0.1;                    
    kIRS1Dephos             = 0.1;                    
    kPI3KPhosByIRS          = 0.1;
    kPI3KDephos             = 0.1;
    kPI3KPhosByRas          = 0.01;
    kPI3KBindWort           = 10;
    kPI3KUnbindWort         = 0.1;
    kPIPPhos                = 0.1;                    
    kPIPDephos              = 0.1;                    
    kPDK1BindPIP3           = 0.01;                        
    kPDK1UnbindPIP3         = 0.1;                        
    kAktBindPIP3            = 0.1;                        
    kAktUnbindPIP3          = 0.1;                        
    kAktPhos                = 0.1;                    
    kAktDephos              = 0.1;                    
    kAktBindMK              = 10;                    
    kTSC2Phos               = 0.1;                    
    kTSC2Dephos             = 0.1;                    
    kRhebLoad               = 2.5;                    
    kRhebUnload             = 5;                    
    kmTORC1CytToLys         = 2;                        
    kmTORC1LysToCyt         = 0.1;                        
    kRAGPhos                = 0.1;                    
    kRAGDephos              = 0.1;                    
    kmTORC1Phos             = 0.01;                    
    kmTORC1Dephos           = 0.1;                        
    kmTORC1BindRapa         = 10;                        
    kmTORC1UnbindRapa       = 0.1;                                                       
    k4EBP1Phos              = 0.1;                    
    k4EBP1Dephos            = 0.1;                        
    kS6KPhos                = 0.4;                    
    kS6KDehos               = 0.1;                    
    kAMPKInhibPhosByAkt     = 0.1;                            
    kAMPKInhibPhosByS6K     = 0.1;                            
    kAMPKDephos             = 0.1;                    
    kAMPKActByCaMKK2        = 0.1;
    kAMPKActByLKB1          = 0.1;
    kAMPKInact              = 0.1;      
    kCaMKK2Act              = 0.1;                    
    kCaMKK2Inact            = 0.1;      
    kAMPPhos                = 0.1;
    kADPDephos              = 0.1;
    kADPPhos                = 0.1;
    kATPDephos              = 0.1;      
    kPKCAct                 = 0.1;
    kPKCActByPMA            = 0.2;
    kPKCInact               = 0.1 ;                 
    kLKB1Act                = 0.1;                    
    kLKB1Inact              = 0.1;                    
    kTKRBindEGF             = 1;                    
    kTKRUnbindEGF           = 0.1;                        
    kTKRBindSOS             = 0.1;                    
    kTKRUnbindSOS           = 0.1;                        
    kSOSPhos                = 1;                    
    kSOSDephos              = 0.1;                    
    kRasLoadByRTK           = 0.1;                    
    kRasLoadByPKC           = 0.1;                    
    kRasUnload              = 0.1;                    
    kRafPhos                = 0.1;                    
    kRafDephos              = 0.1;                    
    kRafDephosByAkt         = 0.1;                    
    kMekPhos                = 0.1;                    
    kMekDephos              = 0.1;                    
    kErkPhos                = 0.01;                    
    kErkDephos              = 0.1;                    
    kMekBindAzd             = 10;                    
    kMekUnbindAzd           = 0.1;                        
    kPLCPhos                = 0.1;                    
    kPLCDephos              = 0.1;                    
    kPLCPhosBasal           = 0.005;                    
    kPIP2Break              = 0.001;                    
    kPIP2form               = 0.1;                    
    kIP3BindIpR             = 0.1;                    
    kIP3UnbindIpR           = 0.1;                        
    kCa2In                  = 0.1;                
    kCa2Out                 = 0.1;                
    kDUSPmRNAIn             = 0.001;
    kDUSPmRNAOut            = 0.1;
    kDUSPIn                 = 0.1;
    kDUSPOut                = 0.01;
    kTSC2InhibitByAAf       = 0.1;
    kTSC2InhibitByAAb       = 0.1;
    kTSC2BindRagGDP         = 0.1;
    kTSC2UnbindRagGDP       = 0.1;
    kRagLoad                = 0.1;

    Insulin                 = 0;        
    AA                      = 0;    
    Rapamycin               = 0;            
    MK2206                  = 0;        
    AZD                     = 0;    
    EGF                     = 0;    
    Wortmannin              = 0;
    PMA                     = 0;

    IRS1                    = 10.001;                        
    IRS1a                   = 0;                        
    pIRS1                   = 0;                        
    PI3K                    = 10.001;                        
    pPI3K                   = 0;                        
    PI3Ki                   = 0;                  
    PTEN                    = 1;      
    PIP2                    = 100.001;                        
    PIP3                    = 0;                        
    PDK1                    = 10.001;                        
    PDK1_PIP3               = 0;                            
    PDK1_PIP3               = 0;                            
    Akt                     = 10.001;                    
    Akt_PIP3                = 0;                            
    pAkt                    = 0;                        
    Akti                    = 0;                        
    TSC2                    = 0;                        
    pTSC2                   = 0;     
    TSC2_Rag                = 10;
    RhebGDP                 = 10.002;                        
    RhebGTP                 = 0;    
    RasGDP                  = 10.002;
    RasGTP                  = 0;                  
    mTORC1cyt               = 10.001;                            
    mTORC1lys               = 0;    
    RagGDP                  = 10.001;
    RagGTP                  = 0;
    mTORC1i                 = 0;                        
    mTORC1ii                = 0;                            
    mTORC1iii               = 0;                            
    pmTORC1                 = 0;                        
    FourEBP1                = 10.001;                            
    pFourEBP1               = 0;                            
    S6K                     = 10.001;                    
    pS6K                    = 0;                        
    AMPK                    = 10.001;                        
    pAMPKi                  = 0;                        
    pAMPK                   = 0;                        
    CaMKK2a                 = 0;                        
    CaMKK2                  = 10.001;        
    PKC                     = 10.001;
    PKCa                    = 0;                   
    LKB1a                   = 0;                        
    LKB1                    = 10.001;                        
    RTK                     = 10.001;                    
    pRTK                    = 0;                        
    pRTKa                   = 0;                        
    Sos                     = 10.001;                    
    pSos                    = 0;                    
    Raf                     = 10.001;                    
    pRaf                    = 0;                        
    Mek                     = 10.001;                    
    pMek                    = 0;                        
    Erk                     = 10.001;                    
    pErk                    = 0;                        
    Meki                    = 0;                        
    PLCeps                  = 10.001;                        
    pPLCeps                 = 0;                        
    IP3                     = 0;                    
    DAG                     = 0;                    
    IpR                     = 10.001;                    
    IpRa                    = 0;                        
    Ca2                     = 0;           
    DUSPmRNA                = 0;
    DUSP                    = 0;         
    AMP                     = 0;
    ADP                     = 0;
    ATP                     = 10;

    R1In        : => IRS1                                   ; Cell * kIRS1In;
    R2Out       : IRS1 =>                                   ; Cell * kIRS1Out*IRS1;
    R1f         : IRS1 => IRS1a                             ; Cell * kIRS1Act*IRS1*Insulin;
    R1b         : IRS1a => IRS1                             ; Cell * kIRS1Inact*IRS1a;
    R1i         : IRS1a => pIRS1                            ; Cell * kIRS1Phos*IRS1a*pS6K;
    R1Out2      : pIRS1 =>                                  ; Cell * kIRS1Dephos*pIRS1;
    R2fi        : PI3K  => pPI3K                            ; Cell * kPI3KPhosByIRS*PI3K*IRS1a;
    R2bi        : pPI3K => PI3K                             ; Cell * kPI3KDephos*pPI3K;
    R2if        : PI3K + Wortmannin => PI3Ki                ; Cell * kPI3KBindWort*PI3K*Wortmannin;
    R2ib        : PI3Ki => PI3K + Wortmannin                ; Cell * kPI3KUnbindWort*PI3Ki;
    R2fii       : PI3K  => pPI3K                            ; Cell * kPI3KPhosByRas*PI3K*RasGTP;
    R3f         : PIP2 => PIP3                              ; Cell * kPIPPhos*PIP2*pPI3K;
    R3b         : PIP3 => PIP2                              ; Cell * kPIPDephos*PIP3*PTEN;
    R4f         : PIP3 + PDK1 => PDK1_PIP3                  ; Cell * kPDK1BindPIP3*PIP3*PDK1;
    R4b         : PDK1_PIP3 => PIP3 + PDK1                  ; Cell * kPDK1UnbindPIP3*PDK1_PIP3;
    R5f         : PIP3 + Akt => Akt_PIP3                    ; Cell * kAktBindPIP3*PIP3*Akt;
    R5b         : Akt_PIP3 => PIP3 + Akt                    ; Cell * kAktUnbindPIP3*Akt_PIP3;
    R6f         : Akt_PIP3 => pAkt                          ; Cell * kAktPhos*Akt_PIP3*PDK1_PIP3;
    R6b         : pAkt => Akt_PIP3                          ; Cell * kAktDephos*pAkt;
    R6i         : Akt + MK2206 => Akti                      ; Cell * kAktBindMK*Akt*MK2206;
    R7f         : TSC2 => pTSC2                             ; Cell * kTSC2Phos*TSC2*pAkt;
    R7b         : pTSC2 => TSC2                             ; Cell * kTSC2Dephos*pTSC2;
    R8f         : TSC2 + RagGDP => TSC2_Rag                 ; Cell * kTSC2BindRagGDP*TSC2*RagGDP;
    R8b         : TSC2_Rag => TSC2 + RagGDP                 ; Cell * kTSC2UnbindRagGDP*TSC2_Rag;
    R9f         : RagGDP => RagGTP                          ; Cell * kRagLoad*RagGDP*AA;
    R10f        : mTORC1cyt + RagGTP => mTORC1lys + RagGDP  ; Cell * kmTORC1CytToLys*mTORC1cyt*RagGTP;
    R10b        : mTORC1lys => mTORC1cyt                    ; Cell * kmTORC1LysToCyt*mTORC1lys;
    R11f        : mTORC1lys + RhebGTP => pmTORC1 + RhebGDP  ; Cell * kmTORC1Phos*mTORC1lys*RhebGTP;
    R11b        : pmTORC1 => mTORC1lys                      ; Cell * kmTORC1Dephos*pmTORC1*AMPK;
    R12f        : RhebGDP => RhebGTP                        ; Cell * kRhebLoad*RhebGDP;
    R12b        : RhebGTP => RhebGDP                        ; Cell * kRhebUnload*RhebGTP*TSC2_Rag;
    R13fi       : mTORC1cyt + Rapamycin => mTORC1i          ; Cell * kmTORC1BindRapa*mTORC1cyt*Rapamycin;
    R13bi       : mTORC1i => mTORC1cyt + Rapamycin          ; Cell * kmTORC1UnbindRapa*mTORC1i;
    R13fii      : mTORC1lys + Rapamycin => mTORC1ii         ; Cell * kmTORC1BindRapa*mTORC1lys*Rapamycin;
    R13bii      : mTORC1ii => mTORC1lys + Rapamycin         ; Cell * kmTORC1UnbindRapa*mTORC1ii;
    R13fiii     : pmTORC1 + Rapamycin => mTORC1iii          ; Cell * kmTORC1BindRapa*pmTORC1*Rapamycin;
    R13biii     : mTORC1iii => pmTORC1 + Rapamycin         ; Cell * kmTORC1UnbindRapa*mTORC1iii;
    R14f        : FourEBP1 => pFourEBP1                     ; Cell * k4EBP1Phos*FourEBP1*pmTORC1;
    R14b        : pFourEBP1 => FourEBP1                     ; Cell * k4EBP1Dephos*pFourEBP1;
    R15f        : S6K => pS6K                               ; Cell * kS6KPhos*S6K*pmTORC1;
    R15b        : pS6K => S6K                               ; Cell * kS6KDehos*pS6K;
    R16fi       : AMPK => pAMPKi                            ; Cell * kAMPKInhibPhosByAkt*AMPK*pAkt;
    R16fii      : AMPK => pAMPKi                            ; Cell * kAMPKInhibPhosByS6K*AMPK*pS6K;
    R16b        : pAMPKi => AMPK                            ; Cell * kAMPKDephos*pAMPKi;
    R17fi       : AMPK => pAMPK                             ; Cell * kAMPKActByCaMKK2*AMPK*CaMKK2a;
    R17fii      : AMPK => pAMPK                             ; Cell * kAMPKActByLKB1*AMPK*LKB1a;
    R17bi       : pAMPK => AMPK                             ; Cell * kAMPKInact*pAMPK;
    R18f        : CaMKK2 => CaMKK2a                         ; Cell * kCaMKK2Act*CaMKK2*Ca2;
    R18b        : CaMKK2a => CaMKK2                         ; Cell * kCaMKK2Inact*CaMKK2a;    
    R19f        : PKC => PKCa                               ; Cell * kPKCAct*PKC*DAG; 
    R19s        : PKC => PKCa                               ; Cell * kPKCActByPMA*PKC*PMA; 
    R19b        : PKCa => PKC                               ; Cell * kPKCInact*PKCa; 
    R20fi       : LKB1 => LKB1a                             ; Cell * kLKB1Act*LKB1*AMP;
    R20fii      : LKB1 => LKB1a                             ; Cell * kLKB1Act*LKB1*ADP;
    R20b        : LKB1a => LKB1                             ; Cell * kLKB1Inact*LKB1a*AA;
    R22f        : RTK => pRTK                               ; Cell * kTKRBindEGF*RTK*EGF;
    R22b        : pRTK => RTK                               ; Cell * kTKRUnbindEGF*pRTK;
    R23f        : pRTK + Sos => pRTKa                       ; Cell * kTKRBindSOS*pRTK*Sos;
    R23b        : pRTKa => pRTK + Sos                       ; Cell * kTKRUnbindSOS*pRTKa;
    R24f        : Sos => pSos                               ; Cell * kSOSPhos*Sos*pErk;
    R24b        : pSos => Sos                               ; Cell * kSOSDephos*pSos;
    R25fi       : RasGDP => RasGTP                          ; Cell * kRasLoadByRTK*RasGDP*pRTKa;
    R25fii      : RasGDP => RasGTP                          ; Cell * kRasLoadByPKC*RasGDP*PKCa;
    R25b        : RasGTP => RasGDP                          ; Cell * kRasUnload*RasGTP;
    R26f        : Raf + RasGTP => pRaf + RasGDP             ; Cell * kRafPhos*Raf*RasGTP;
    R26b        : pRaf => Raf                               ; Cell * kRafDephos*pRaf;
    R26b        : pRaf => Raf                               ; Cell * kRafDephosByAkt*pRaf*pAkt;
    R27f        : Mek => pMek                               ; Cell * kMekPhos*Mek*pRaf;
    R27b        : pMek => Mek                               ; Cell * kMekDephos*pMek;
    R28f        : Erk => pErk                               ; Cell * kErkPhos*Erk*pMek;
    R28b        : pErk => Erk                               ; Cell * kErkDephos*pErk*DUSP;
    R29f        : Mek => Meki                               ; Cell * kMekBindAzd*Mek*AZD;
    R29b        : Meki => Mek                               ; Cell * kMekUnbindAzd*Meki;
    R30In       : => DUSPmRNA                               ; Cell * kDUSPmRNAIn*pErk;
    R30OUT      : DUSPmRNA =>                               ; Cell * kDUSPmRNAOut*DUSPmRNA;
    R31In       : => DUSP                                   ; Cell * kDUSPIn*DUSPmRNA;
    R31OUT      : DUSP =>                                   ; Cell * kDUSPOut*DUSP;
    R32f        : PLCeps + RasGTP => pPLCeps + RasGDP       ; Cell * kPLCPhos*PLCeps*RasGTP;
    R32f        : PLCeps => pPLCeps                         ; Cell * kPLCPhosBasal*PLCeps*RasGTP;
    R32b        : pPLCeps => PLCeps                         ; Cell * kPLCDephos*pPLCeps;
    R33f        : PIP2 => IP3 + DAG                         ; Cell * kPIP2Break*PIP2*pPLCeps;
    R33b        : IP3 + DAG => PIP2                         ; Cell * kPIP2form*IP3*DAG;
    R34f        : IP3 + IpR => IpRa                         ; Cell * kIP3BindIpR*IP3*IpR;
    R34b        : IpRa => IP3 + IpR                         ; Cell * kIP3UnbindIpR*IpRa;
    R35f        : => Ca2                                    ; Cell * kCa2In*IpRa;
    R35b        : Ca2 =>                                    ; Cell * kCa2Out*Ca2;
end

"""






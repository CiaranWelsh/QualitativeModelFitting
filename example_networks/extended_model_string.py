model_string = f"""
function CompetitiveInhibitionWithKcat(km, ki, kcat, E, I, S)
    kcat * E * S / (km + S + ((km * I )/ ki)  )
end    

function CompetitiveInhibition(Vmax, km, ki, I, S)
    Vmax * S / (km + S + ((km * I )/ ki)  )
end

function MMWithKcat(km, kcat, S, E)
    kcat * E * S / (km + S)
end


model ComplexModel
    compartment Cell=1;
    var IRS1           in Cell;
    var IRS1a          in Cell;
    var pIRS1          in Cell;
    var PI3K           in Cell;
    var pPI3K          in Cell;
    var PI3Ki          in Cell;
    var PIP2           in Cell;
    var PIP3           in Cell;
    var PDK1           in Cell;
    var PDK1_PIP3      in Cell;
    var Akt            in Cell;
    var Akt_PIP3       in Cell;
    var pAkt           in Cell;
    var Akt_PIP3       in Cell;
    var Akti           in Cell;
    var TSC2           in Cell;
    var pTSC2          in Cell;
    var RagGDP         in Cell;
    var TSC2_Rag       in Cell;
    var RagGTP         in Cell;
    var mTORC1cyt      in Cell;
    var mTORC1lys      in Cell;
    var RhebGTP        in Cell;
    var pmTORC1        in Cell;
    var RhebGDP        in Cell;
    var mTORC1i        in Cell;
    var mTORC1ii       in Cell;
    var mTORC1iii      in Cell;
    var FourEBP1       in Cell;
    var pFourEBP1      in Cell;
    var S6K            in Cell;
    var pS6K           in Cell;
    var AMPK           in Cell;
    var AMPKi         in Cell;
    var pAMPK          in Cell;
    var CaMKK2         in Cell;
    var CaMKK2a        in Cell;
    var Ca2            in Cell;
    var PKC            in Cell;
    var PKCa           in Cell;
    var RTK            in Cell;
    var pRTK           in Cell;
    var Sos            in Cell;
    var pRTKa          in Cell;
    var pSos           in Cell;
    var RasGDP         in Cell;
    var RasGTP         in Cell;
    var Raf            in Cell;
    var pRaf           in Cell;
    var Mek            in Cell;
    var pMek           in Cell;
    var Erk            in Cell;
    var pErk           in Cell;
    var Meki           in Cell;
    var DUSPmRNA       in Cell;
    var DUSP           in Cell;
    var PLCeps         in Cell;
    var pPLCeps        in Cell;
    var IP3            in Cell;
    var DAG            in Cell;
    var IpR            in Cell;
    var IpRa           in Cell;
    var E2             in Cell;
    var E2_cyt         in Cell;
    var ERa_cyt        in Cell;
    var ERa_E2         in Cell;
    var ERa_dimer      in Cell;
    var ERa_dimer_nuc  in Cell;
    var ERa_nuc        in Cell;
    var TFFmRNA        in Cell;
    var Greb1mRNA      in Cell;
    var TFF            in Cell;
    var Greb1          in Cell;
    var ProlifSignals  in Cell;
    var Growth         in Cell;
    var Immuno         in Cell;
    var pJak           in Cell;
    var Jak            in Cell;
    var Stat1          in Cell;
    var pStat1         in Cell;
    var pStat1_dim_cyt in Cell;
    var pStat1_dim_nuc in Cell;
    var IDO1mRNA       in Cell;
    var IDO1           in Cell;
    var Kyn            in Cell;
    var GCN2           in Cell;
    var GCN2a         in Cell;
    var eIFa           in Cell;
    var peIFa          in Cell;
    var PTEN           in Cell;
    var LKB1           in Cell;
    var LKB1_nuc        in Cell;
    var ERa_cyti        in Cell;
    var Trp             in Cell;
    var Ulk             in Cell;
    var pUlk                in Cell;
    var Autophagy               in Cell;


    const Fulvestrant ;
    const Rapamycin   ;
    const Insulin;
    // const AA                      
    const Rapamycin               
    const MK2206                  
    const AZD                     
    const EGF                     
    const Wortmannin              
    const PMA                     
    const IGF                     
    const INFg                    
    const Feeding                 

    kIRS1Act                = 0.1;         
    kIRS1Inact              = 0.1;         
    kIRS1Phos               = 0.1;         
    kIRS1Dephos             = 0.1; 
    kPI3KPhosByIRS1a        = 0.1;        
    kPI3KDephos             = 0.1;         
    kPI3KPhosByIGF          = 0.1;             
    kPI3KPhosByGreb1        = 0.1;                 
    kPI3KPhosByRas          = 0.1;             
    kPIPPhos                = 1;         
    kPIPDephos              = 0.1;         
    kPDK1BindPIP3           = 0.1;             
    kPDK1UnbindPIP3         = 0.1;             
    kAktBindPIP3            = 0.1;             
    kAktUnbindPIP3          = 0.1;             
    kAktPhos                = 1;         
    kAktDephos              = 0.1;         
    
    kTSC2Phos               = 0.1;         
    kTSC2Dephos             = 0.1;         
    kTSC2BindRagGDP         = 0.1;             
    kTSC2UnbindRagGDP       = 0.1;                 
    kRagLoad                = 0.1;         
    kmTORC1CytToLys         = 0.1;             
    kmTORC1LysToCyt         = 0.1;             
    kmTORC1Phos             = 0.1;         
    kmTORC1Dephos           = 0.1;             
    kRhebLoad               = 0.1;         
    kRhebUnload             = 0.1;  
    k4EBP1Phos              = 0.1;         
    k4EBP1Dephos            = 0.1;             
    kS6KPhos                = 0.1;         
    kS6KDehos               = 0.1;         
    
    // ampk parameters
    kAMPKInhibByAkt         = 0.1;
    kAMPKDephos             = 0.1;
    kAMPKPhosByLKB1         = 0.1;
    kAMPKPhosByCaMKK2a      = 0.1;
    kAMPKInact              = 0.1;
    kLKB1ToCyt              = 0.1;
    kLKB1ToNuc              = 1;
    kCaMKK2Act              = 0.1;         
    kCaMKK2Inact            = 0.1;             
    kUlkPhos                = 0.1;
    kUlkDephos                = 0.1;
    kAutophagyIn            = 0.1;
    kAutophagyOut           = 0.1;

    kPKCAct                 = 0.1;     
    kPKCActByPMA            = 0.1;             
    kPKCInact               = 0.1;         
    kTKRBindEGF             = 0.1;         
    kTKRUnbindEGF           = 0.1;             
    kTKRBindSOS             = 0.1;         
    kTKRUnbindSOS           = 0.1;             
    kSOSPhos                = 0.1;         
    kSOSDephos              = 0.1;         
    kRasLoadByRTK           = 0.1;             
    kRasLoadByPKC           = 0.1;             
    kRasUnload              = 0.1;         
    kRafPhos                = 0.1;         
    kRafDephos              = 0.1;         
    kRafDephosByAkt         = 0.1;             
    kMekPhos                = 0.1;         
    kMekDephos              = 0.1;         
    kErkPhos                = 0.1;         
    kErkDephos              = 0.1;         
    kDUSPmRNAIn             = 0.01;         
    kDUSPmRNAOut            = 0.1;             
    kDUSPIn                 = 0.01;     
    kDUSPOut                = 0.1;         
    kPLCPhos                = 0.1;         
    kPLCPhosBasal           = 0.1;             
    kPLCDephos              = 0.1;         
    kPIP2Break              = 0.1;         
    kPIP2form               = 0.1;         
    kIP3BindIpR             = 0.1;         
    kIP3UnbindIpR           = 0.1;             
    kCa2In                  = 0.1;     
    kCa2Out                 = 0.1;     
    kE2ToCyt                = 1;         
    kE2CytToEx              = 0.1;         
    kE2BindER               = 1;         
    kE2UnbindER             = 0.1;         
    kERDim                  = 0.1;     
    kERUndim                = 0.1;         
    kERCytToNuc             = 0.1;         
    kERNucToCyt             = 0.1;         
    kERDimUnbind            = 0.1;             
    kERDimBind              = 0.1;         
    kTFFmRNAIn              = 0.1;         
    kTFFmRNAOut             = 0.1;         
    kGreb1mRNAIn            = 0.1;             
    kGreb1mRNAOut           = 0.1;             
    kTFFIn                  = 0.1;     
    kTFFOut                 = 0.1;     
    kGreb1In                = 0.1;         
    kGreb1Out               = 0.1;         
    kProlifSignalIn         = 0.1;             
    kProlifSignalIn         = 0.1;             
    kProlifSignalOut        = 0.1;                 
    kGrowthBasal            = 0.01;             
    kGrowthActive           = 0.1;             
    kGrowthInhibBasal       = 0.1;                 
    kGrowthInhibActive      = 0.1;                 
    kImmunoInBasal          = 0.1;             
    kImmunoInActive         = 0.1;             
    kImmunoOut              = 0.1;         
    kJakPhos                = 0.1;         
    kJakDephos              = 0.1;         
    kStat1Phos              = 0.1;         
    kStat1Dephos            = 0.1;             
    kStat1Dim               = 0.1;         
    kStat1Undim             = 0.1;         
    kStat1DimToNuc          = 1;             
    kStat1DimToCyt          = 0.1;             
    kIDO1mRNAIn             = 0.01;         
    kIDO1mRNAOut            = 0.1;             
    kIDO1In                 = 0.1;     
    kIDO1Out                = 0.01;         
    kAAToKyn                = 10;
    kKynToAA                = 0.1;         
    kAAIn                   = 1;     
    kAAOut                  = 0.1;     
    kGCN2Act                = 0.1;         
    kGCN2Inact              = 0.1;         
    keIFaPhos               = 0.5;         
    keIFaDephos             = 0.1;    
    kAASuffIn               = 0.1;
    kAASuffOut              = 0.1;
    
    // inhibitor reaction constants
    kPI3KBindWort           = 100;
    kPI3KUnbindWort         = 0.1;   
    kMekBindAZD             = 100;
    kMekUnbindAZD           = 0.1;
    kmTORC1BindRapa         = 100;
    kAktUnbindMK            = 0.1;     
    kmTORC1BindRapa         = 100;
    kmTORC1UnbindRapa       = 0.1;
    kERaBindFulv            = 100;
    kERaUnbindFulv          = 0.1;
    kTrpIn                  = 0.3;
    kTrpOut                 = 0.1;
    kAktBindMK              = 100;         
    kAktUnbindMK            = 0.1;         
    

    // inputs
    Insulin                 = 0;        
    Feeding                 = 0;
    Rapamycin               = 0;            
    Fulvestrant             = 0;
    MK2206                  = 0;        
    AZD                     = 0;    
    EGF                     = 0;    
    Wortmannin              = 0;
    PMA                     = 0;
    IGF                     = 0;
    INFg                    = 0;
    E2                      = 0;
    
    // model components
    IRS1                    = 10;                        
    IRS1a                   = 0;                        
    pIRS1                   = 0;                        
    PI3K                    = 10;                        
    pPI3K                   = 0;                        
    PI3Ki                   = 0;                        
    PIP2                    = 10;                        
    PIP3                    = 0;                        
    PDK1                    = 10;                        
    PDK1_PIP3               = 0;                            
    Akt                     = 10;                    
    Akt_PIP3                = 0;                            
    pAkt                    = 0;                        
    Akt_PIP3                = 0;                            
    Akti                    = 0;                        
    TSC2                    = 0;                        
    pTSC2                   = 0;                        
    RagGDP                  = 10;                        
    TSC2_Rag                = 10;                            
    RagGTP                  = 0;                        
    mTORC1cyt               = 10;                            
    mTORC1lys               = 0;                            
    RhebGTP                 = 0;                        
    pmTORC1                 = 0;                        
    RhebGDP                 = 10;                        
    mTORC1i                 = 0;                        
    mTORC1ii                = 0;                            
    mTORC1iii               = 0;                            
    FourEBP1                = 10;                            
    pFourEBP1               = 0;                            
    S6K                     = 10;                    
    pS6K                    = 0;                        
    AMPK                    = 10;                        
    AMPKi                  = 0;                        
    pAMPK                   = 0;                        
    CaMKK2                  = 10;                        
    CaMKK2a                 = 0;      
    LKB1_nuc                = 0;
    LKB1                    = 10;                  
    Ca2                     = 0;
    PKC                     = 10;                    
    PKCa                    = 0;                        
    RTK                     = 10;                    
    pRTK                    = 0;                        
    Sos                     = 10;                    
    pRTKa                   = 0;                        
    pSos                    = 0;                        
    RasGDP                  = 10;                        
    RasGTP                  = 0;                        
    Raf                     = 10;                    
    pRaf                    = 0;                        
    Mek                     = 10;                    
    pMek                    = 0;                        
    Erk                     = 10;                    
    pErk                    = 0;                        
    Meki                    = 0;                        
    DUSPmRNA                = 0;                            
    DUSP                    = 0;                        
    PLCeps                  = 10;                        
    pPLCeps                 = 0;                        
    IP3                     = 0;                    
    DAG                     = 0;                    
    IpR                     = 10;                    
    IpRa                    = 0;                        
    E2_cyt                  = 0;                        
    ERa_cyt                 = 10;       
    ERa_cyti                = 0;                 
    ERa_E2                  = 0;                        
    ERa_dimer               = 0;                            
    ERa_dimer_nuc           = 0;                               
    ERa_nuc                 = 0;                        
    TFFmRNA                 = 0;                        
    Greb1mRNA               = 0;                            
    TFF                     = 0;                    
    Greb1                   = 0;                        
    ProlifSignals           = 0;                              
    Growth                  = 0;                        
    Immuno                  = 0;                        
    pJak                    = 0;                        
    Jak                     = 10;                    
    Stat1                   = 10;                        
    pStat1                  = 0;                        
    pStat1_dim_cyt          = 0;                              
    pStat1_dim_nuc          = 0;                              
    IDO1mRNA                = 0;                            
    IDO1                    = 0;                        
    Kyn                     = 0;                    
    GCN2                    = 10;                        
    GCN2a                  = 0;                        
    eIFa                    = 10;                        
    peIFa                   = 0; 
    PTEN                    = 10;                       
    Trp                     = 0;              
    Ulk                     = 10;        
    pUlk                    = 0;            
    Autophagy               = 0;                

    // reactions
    // PI3K reactions
    R1f         : IRS1 => IRS1a                             ; Cell * kIRS1Act*IRS1*Insulin;
    R1b         : IRS1a => IRS1                             ; Cell * kIRS1Inact*IRS1a;
    R1i         : IRS1a => pIRS1                            ; Cell * kIRS1Phos*IRS1a*pS6K;
    R1Out2      : pIRS1 => IRS1                             ; Cell * kIRS1Dephos*pIRS1;
    R2fIRS      : PI3K  => pPI3K                            ; Cell * kPI3KPhosByIRS1a*PI3K*IRS1a;
    R2b         : pPI3K => PI3K                             ; Cell * kPI3KDephos*pPI3K;
    R2if        : PI3K => PI3Ki                             ; Cell * kPI3KBindWort*PI3K*Wortmannin;
    R2ib        : PI3Ki => PI3K                             ; Cell * kPI3KUnbindWort*PI3Ki;
    R2fIGF      : PI3K  => pPI3K                            ; Cell * kPI3KPhosByIGF*PI3K*IGF;
    R2fGreb1    : PI3K  => pPI3K                            ; Cell * kPI3KPhosByGreb1*PI3K*Greb1;
    R2fRas      : PI3K  => pPI3K                            ; Cell * kPI3KPhosByRas*PI3K*RasGTP;
    R3f         : PIP2 => PIP3                              ; Cell * kPIPPhos*PIP2*pPI3K;
    R3b         : PIP3 => PIP2                              ; Cell * kPIPDephos*PIP3*PTEN;
    R4f         : PIP3 + PDK1 => PDK1_PIP3                  ; Cell * kPDK1BindPIP3*PIP3*PDK1;
    R4b         : PDK1_PIP3 => PIP3 + PDK1                  ; Cell * kPDK1UnbindPIP3*PDK1_PIP3;
    R5f         : PIP3 + Akt => Akt_PIP3                    ; Cell * kAktBindPIP3*PIP3*Akt;
    R5b         : Akt_PIP3 => PIP3 + Akt                    ; Cell * kAktUnbindPIP3*Akt_PIP3;
    R6f         : Akt_PIP3 => pAkt                          ; Cell * kAktPhos*Akt_PIP3
    R6b         : pAkt => Akt_PIP3                          ; Cell * kAktDephos*pAkt;
    R6if        : Akt => Akti                               ; Cell * kAktBindMK*Akt*MK2206;
    R6ib        : Akti => Akt                               ; Cell * kAktUnbindMK*Akti;
    R7f         : TSC2 => pTSC2                             ; Cell * kTSC2Phos*TSC2*pAkt;
    R7b         : pTSC2 => TSC2                             ; Cell * kTSC2Dephos*pTSC2;
    R8f         : TSC2 + RagGDP => TSC2_Rag                 ; Cell * kTSC2BindRagGDP*TSC2*RagGDP;
    R8b         : TSC2_Rag => TSC2 + RagGDP                 ; Cell * kTSC2UnbindRagGDP*TSC2_Rag*pAkt;
    R9f         : RagGDP => RagGTP                          ; Cell * kRagLoad*RagGDP*Trp;
    R10f        : mTORC1cyt + RagGTP => mTORC1lys + RagGDP  ; Cell * kmTORC1CytToLys*mTORC1cyt*RagGTP;
    R10b        : mTORC1lys => mTORC1cyt                    ; Cell * kmTORC1LysToCyt*mTORC1lys;
    R11f        : mTORC1lys + RhebGTP => pmTORC1 + RhebGDP  ; Cell * kmTORC1Phos*mTORC1lys*RhebGTP;
    R11b        : pmTORC1 => mTORC1lys                      ; Cell * kmTORC1Dephos*pmTORC1*AMPK;
    R12f        : RhebGDP => RhebGTP                        ; Cell * kRhebLoad*RhebGDP;
    R12b        : RhebGTP => RhebGDP                        ; Cell * kRhebUnload*RhebGTP*TSC2_Rag;
    R13fi       : mTORC1cyt  => mTORC1i                     ; Cell * kmTORC1BindRapa*mTORC1cyt*Rapamycin;
    R13bi       : mTORC1i => mTORC1cyt                      ; Cell * kmTORC1UnbindRapa*mTORC1i;
    R13fii      : mTORC1lys  => mTORC1ii                    ; Cell * kmTORC1BindRapa*mTORC1lys*Rapamycin;
    R13bii      : mTORC1ii => mTORC1lys                     ; Cell * kmTORC1UnbindRapa*mTORC1ii;
    R13fiii     : pmTORC1  => mTORC1iii                     ; Cell * kmTORC1BindRapa*pmTORC1*Rapamycin;
    R13biii     : mTORC1iii => pmTORC1                      ; Cell * kmTORC1UnbindRapa*mTORC1iii;
    R14f        : FourEBP1 => pFourEBP1                     ; Cell * k4EBP1Phos*FourEBP1*pmTORC1;
    R14b        : pFourEBP1 => FourEBP1                     ; Cell * k4EBP1Dephos*pFourEBP1;
    R15f        : S6K => pS6K                               ; Cell * kS6KPhos*S6K*pmTORC1;
    R15b        : pS6K => S6K                               ; Cell * kS6KDehos*pS6K;
    
    // AMPK reactions
    
    R16AMPKif   : AMPK => AMPKi                             ; Cell * kAMPKInhibByAkt*AMPK*pAkt;
    R16AMPKib   : AMPKi => AMPK                             ; Cell * kAMPKDephos*AMPKi;    
    R17f1       : AMPK => pAMPK                             ; Cell * kAMPKPhosByLKB1*AMPK*LKB1
    R17f2       : AMPK => pAMPK                             ; Cell * kAMPKPhosByCaMKK2a*AMPK*CaMKK2a
    R19f        : LKB1_nuc => LKB1                          ; Cell * kLKB1ToCyt*LKB1_nuc;
    R19b        : LKB1 => LKB1_nuc                          ; Cell * kLKB1ToNuc*LKB1*Feeding;
    R20f        : CaMKK2 => CaMKK2a                         ; Cell * kCaMKK2Act*CaMKK2*Ca2;
    R20b        : CaMKK2a => CaMKK2                         ; Cell * kCaMKK2Inact*CaMKK2a;    
    R21f        : Ulk => pUlk                               ; Cell * kUlkPhos*Ulk*pAMPK;
    R21b        : pUlk => Ulk                               ; Cell * kUlkDephos*pUlk;
    R21f2       : => Autophagy                              ; Cell * kAutophagyIn*pUlk
    R21b2       : Autophagy =>                              ; Cell * kAutophagyOut*Autophagy

     
    // Erk pathway
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
    R27if       : Mek -> Meki                               ; Cell * kMekBindAZD*Mek*AZD;
    R27ib       : Meki -> Mek                               ; Cell * kMekUnbindAZD*Meki;
    R28f        : Erk => pErk                               ; Cell * kErkPhos*Erk*pMek;
    R28b        : pErk => Erk                               ; Cell * kErkDephos*pErk*DUSP;
    R30In       : => DUSPmRNA                               ; Cell * kDUSPmRNAIn*pErk;
    R30OUT      : DUSPmRNA =>                               ; Cell * kDUSPmRNAOut*DUSPmRNA;
    R31In       : => DUSP                                   ; Cell * kDUSPIn*DUSPmRNA;
    R31OUT      : DUSP =>                                   ; Cell * kDUSPOut*DUSP;
    
    // IP pathway
    R32f        : PLCeps + RasGTP => pPLCeps + RasGDP       ; Cell * kPLCPhos*PLCeps*RasGTP;
    R32f        : PLCeps => pPLCeps                         ; Cell * kPLCPhosBasal*PLCeps*RasGTP;
    R32b        : pPLCeps => PLCeps                         ; Cell * kPLCDephos*pPLCeps;
    R33f        : PIP2 => IP3 + DAG                         ; Cell * kPIP2Break*PIP2*pPLCeps;
    R33b        : IP3 + DAG => PIP2                         ; Cell * kPIP2form*IP3*DAG;
    R34f        : IP3 + IpR => IpRa                         ; Cell * kIP3BindIpR*IP3*IpR;
    R34b        : IpRa => IP3 + IpR                         ; Cell * kIP3UnbindIpR*IpRa;
    R35f        : => Ca2                                    ; Cell * kCa2In*IpRa;
    R35b        : Ca2 =>                                    ; Cell * kCa2Out*Ca2;
    R36f1       : PKC => PKCa                               ; Cell * kPKCAct*PKC*DAG; 
    R36f2       : PKC => PKCa                               ; Cell * kPKCActByPMA*PKC*PMA; 
    R36b        : PKCa => PKC                               ; Cell * kPKCInact*PKCa; 
    
    // Estrogen pathway
    R37f        : E2 => E2_cyt                              ; Cell * kE2ToCyt*E2;
    R37b        : E2_cyt => E2                              ; Cell * kE2CytToEx*E2_cyt;
    R38f        : ERa_cyt + E2_cyt  => ERa_E2               ; Cell * kE2BindER*ERa_cyt*E2_cyt;
    R38b        : ERa_E2 => ERa_cyt + E2_cyt                ; Cell * kE2UnbindER*ERa_E2;
    R39if       : ERa_cyt => ERa_cyti                       ; Cell * kERaBindFulv*ERa_cyt*Fulvestrant;
    R39ib       : ERa_cyti => ERa_cyt                       ; Cell * kERaUnbindFulv*ERa_cyti;
    R40f        : ERa_E2 + ERa_E2 => ERa_dimer              ; Cell * kERDim*ERa_E2*ERa_E2;
    R40b        : ERa_dimer => ERa_E2 + ERa_E2              ; Cell * kERUndim*ERa_dimer;
    R41f        : ERa_dimer => ERa_dimer_nuc                ; Cell * kERCytToNuc*ERa_dimer;
    R41b        : ERa_dimer_nuc => ERa_dimer                ; Cell * kERNucToCyt*ERa_dimer_nuc;
    R42f        : ERa_dimer_nuc => ERa_nuc + ERa_nuc        ; Cell * kERDimUnbind*ERa_dimer_nuc;
    R42b        : ERa_nuc + ERa_nuc  => ERa_dimer_nuc       ; Cell * kERDimBind*ERa_nuc*ERa_nuc;
    R43In       : => TFFmRNA                                ; Cell * kTFFmRNAIn*ERa_dimer_nuc
    R43Out      : TFFmRNA =>                                ; Cell * kTFFmRNAOut*TFFmRNA
    R44In       : => Greb1mRNA                              ; Cell * kGreb1mRNAIn*ERa_dimer_nuc
    R44Out      : Greb1mRNA =>                              ; Cell * kGreb1mRNAOut*Greb1mRNA
    R45In       : => TFF                                    ; Cell * kTFFIn*TFFmRNA*eIFa
    R45Out      : TFF =>                                    ; Cell * kTFFOut*TFF
    R46In       : => Greb1                                  ; Cell * kGreb1In*Greb1mRNA*eIFa
    R46Out      : Greb1 =>                                  ; Cell * kGreb1Out*Greb1
    
    
    // growth module
    R46In1      : => ProlifSignals                          ; Cell * kProlifSignalIn*ERa_dimer_nuc
    R46In2      : => ProlifSignals                          ; Cell * kProlifSignalIn*pS6K
    R46Out      : ProlifSignals =>                          ; Cell * kProlifSignalOut*ProlifSignals
    R47In1      : => Growth                                 ; Cell * kGrowthBasal
    R47In2      : => Growth                                 ; Cell * kGrowthActive*ProlifSignals
    R47Out1     : Growth =>                                 ; Cell * kGrowthInhibBasal*Growth
    R47Out2     : Growth =>                                 ; Cell * kGrowthInhibActive*Growth*Immuno
    R48In1      : => Immuno                                 ; Cell * kImmunoInBasal
    R48In2      : => Immuno                                 ; Cell * kImmunoInActive*Kyn
    R48Out      : Immuno =>                                 ; Cell * kImmunoOut*Immuno
    
    // INFg system
    R49f        : Jak => pJak                               ; Cell * kJakPhos*Jak*INFg
    R49b        : pJak => Jak                               ; Cell * kJakDephos*pJak
    R50f        : Stat1 => pStat1                           ; Cell * kStat1Phos*Stat1*pJak
    R50b        : pStat1 => Stat1                           ; Cell * kStat1Dephos*pStat1
    R51f        : pStat1 + pStat1 => pStat1_dim_cyt         ; Cell * kStat1Dim*pStat1^2
    R51b        : pStat1_dim_cyt => pStat1 + pStat1         ; Cell * kStat1Undim*pStat1_dim_cyt
    R52f        : pStat1_dim_cyt => pStat1_dim_nuc          ; Cell * kStat1DimToNuc*pStat1_dim_cyt
    R52b        : pStat1_dim_nuc => pStat1_dim_cyt          ; Cell * kStat1DimToCyt*pStat1_dim_nuc
    
    // Trp stuff
    R53In       : => IDO1mRNA                               ; Cell * kIDO1mRNAIn*pStat1_dim_nuc
    R53Out      : IDO1mRNA =>                               ; Cell * kIDO1mRNAOut*IDO1mRNA
    R54In       : => IDO1                                   ; Cell * kIDO1In*IDO1mRNA*eIFa
    R54Out      : IDO1 =>                                   ; Cell * kIDO1Out*IDO1
    R55f        : Trp => Kyn                                ; Cell * kAAToKyn*Trp*IDO1;
    R55b        : Kyn => Trp                                ; Cell * kKynToAA*Kyn
    R56f        : GCN2a => GCN2                             ; Cell * kGCN2Act*GCN2a*Trp 
    R56b        : GCN2 => GCN2a                             ; Cell * kGCN2Inact*GCN2
    R57f        : eIFa => peIFa                             ; Cell * keIFaPhos*eIFa*GCN2a
    R57b        : peIFa => eIFa                             ; Cell * keIFaDephos*peIFa
    R58f        : => Trp                                    ; Cell * kTrpIn*Feeding;
    R58b        : Trp =>                                    ; Cell * kTrpOut*Trp;
end

"""

if __name__ == '__main__':
    import tellurium
    import pycotools3 as py3
    import os
    copasi_file = os.path.join(os.path.dirname(__file__), 'copasi_model.cps')
    mod = py3.model.loada(model_string, copasi_file)
    mod.open()

    # mod = tellurium.loada(model_string)
    # mod.simulate(0, 100, 101)



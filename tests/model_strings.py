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

MODEL1 = f"""

{functions}

model ModelWithMTOR()
    compartment       Cell = 1;
    var IRS1          in Cell;
    var IRS1a        in Cell;
    var pIRS1         in Cell; 
    var Akt           in Cell;
    var pAkt          in Cell;
    var TSC2          in Cell;
    var pTSC2         in Cell;
    var RhebGDP       in Cell;
    var RhebGTP       in Cell;
    var Pras40        in Cell;
    var mTORC1_Pras40_Lys in Cell;
    var mTORC1_Pras40_Cyt in Cell;
    var pmTORC1        in Cell;
    var pmTORC1       in Cell;
    var mTORC1_i      in Cell;
    var mTORC1_ii     in Cell;
    var mTORC1_iii     in Cell;
    var S6K           in Cell;
    var pS6K          in Cell;
    var FourEBP1      in Cell;
    var pFourEBP1     in Cell;
    _const Rapamycin;    
    _const Insulin; 

    kIRS1In             = 1;
    kIRS1Out            = 0.1;
    kIRS1Act_km         = 1;
    kIRS1Act_kcat       = 10;
    kIRS1Act_h          = 2;
    kIRS1Act            = 0.1;
    kIRS1Inact          = 0.1;
    kIRS1Phos           = 0.5;
    kIRS1Dephos         = 0.1;
    kAktPhos            = 0.1;
    kAktDephos          = 0.1;
    kTSC2Phos           = 0.1;
    kTSC2Dephos         = 0.1;
    kmTORC1ToLys        = 0.1;
    kmTORC1ToCyt        = 0.1;
    kmTORC1Act          = 0.001;
    kmTORC1Dephos       = 1;
    kmTORC1BindRapa     = 2.0;
    kmTORC1UnbindRapa   = 0.1;
    kS6KPhos_km         = 100;
    kS6KPhos_kcat       = 2;
    kS6KDephos          = 0.1;
    k4Phos_km           = 5;
    k4EBP1Phos_kcat     = 5;
    k4EBP1Dephos        = 0.1;
    kRhebLoad           = 0.01;
    kRhebUnload         = 10;
    kmTORC1BindPras40   = 0.1;
    kPras40Dephos       = 0.1;

    Rapamycin           = 0;
    Insulin             = 0;
    AA                  = 1;
    IRS1 = 10.000001549282924;
    IRS1a = 0                                                  
    pIRS1 = 0                                                   
    Akt = 10.005001550057566;
    pAkt = 0                                                    
    TSC2 = 10.005001550057566;
    pTSC2 = 0.0;
    RhebGDP = 90.91323534809237;
    RhebGTP = 9.086780144736869;
    Pras40 = 8.659321556325276e-09;
    mTORC1_Pras40_Lys = 5.012500772248403;
    mTORC1_Pras40_Cyt = 5.012500772248403;
    pmTORC1 = 0                                                 
    mTORC1_i = 0                                                
    mTORC1_ii = 0                                               
    mTORC1_iii = 0                                              
    S6K = 10.005001534306187;
    pS6K = 0                           
    FourEBP1 = 10                           
    pFourEBP1 = 0                         
    ppPras40 =   0                        
    Rapamycin = 0.0;

    // observables
    // MM(km, Vmax, S)
    // MMWithKcat(km, kcat, S, E)
    // Hill(km, kcat, L, S, h) or Hill(km, kcat, E, S, h)
    R1In    : => IRS1                                               ; Cell * kIRS1In;
    R2Out   : IRS1 =>                                               ; Cell * kIRS1Out*IRS1;
    R1f     : IRS1 => IRS1a                                        ; Cell * kIRS1Act*IRS1*Insulin;//Hill(kIRS1Act_km, kIRS1Act_kcat, Insulin, IRS1, kIRS1Act_h);
    R1b     : IRS1a => IRS1                                        ; Cell * kIRS1Inact*IRS1a;
    R1i     : IRS1a => pIRS1                                       ; Cell * kIRS1Phos*IRS1a*pS6K;
    R1o     : pIRS1 =>                                              ; Cell * kIRS1Dephos*pIRS1;
    R2f     : Akt => pAkt                                           ; Cell * kAktPhos*Akt*IRS1a;
    R2b     : pAkt => Akt                                           ; Cell * kAktDephos*pAkt;
    R3f     : TSC2 => pTSC2                                         ; Cell * kTSC2Phos*TSC2*pAkt;
    R3b     : pTSC2 => TSC2                                         ; Cell * kTSC2Dephos*pTSC2;
    R4f     : RhebGDP => RhebGTP                                    ; Cell * kRhebLoad*RhebGDP*AA;
    R4b     : RhebGTP => RhebGDP                                    ; Cell * kRhebUnload*RhebGTP*TSC2;
    R5f     : mTORC1_Pras40_Cyt => mTORC1_Pras40_Lys                ; Cell * kmTORC1ToLys*mTORC1_Pras40_Cyt*AA;
    R5b     : mTORC1_Pras40_Lys => mTORC1_Pras40_Cyt                ; Cell * kmTORC1ToCyt*mTORC1_Pras40_Lys;
    R6f     : mTORC1_Pras40_Lys + RhebGTP => pmTORC1 + ppPras40 + RhebGDP ; Cell * kmTORC1Act*pAkt*RhebGTP*mTORC1_Pras40_Lys;
    R6b     : pmTORC1 + Pras40 => mTORC1_Pras40_Lys                  ; Cell * kmTORC1BindPras40*pmTORC1*Pras40;
    R6c     : ppPras40 => Pras40                                    ; Cell * kPras40Dephos*ppPras40;
    R7if    : mTORC1_Pras40_Cyt + Rapamycin => mTORC1_i             ; Cell * kmTORC1BindRapa*mTORC1_Pras40_Cyt*Rapamycin;
    R7ib    : mTORC1_i => mTORC1_Pras40_Cyt + Rapamycin             ; Cell * kmTORC1UnbindRapa*mTORC1_i;
    R8iif   : mTORC1_Pras40_Lys + Rapamycin => mTORC1_ii            ; Cell * kmTORC1BindRapa*mTORC1_Pras40_Lys*Rapamycin;
    R8iib   : mTORC1_ii => mTORC1_Pras40_Lys + Rapamycin            ; Cell * kmTORC1UnbindRapa*mTORC1_ii;
    R9iiif  : pmTORC1 + Rapamycin => mTORC1_iii                      ; Cell * kmTORC1BindRapa*pmTORC1*Rapamycin;
    R9iiib  : mTORC1_iii => pmTORC1 + Rapamycin                      ; Cell * kmTORC1UnbindRapa*mTORC1_iii;
    R10f     : S6K => pS6K                                          ; Cell * MMWithKcat(kS6KPhos_km, kS6KPhos_kcat, S6K, pmTORC1);
    R10b     : pS6K => S6K                                          ; Cell * kS6KDephos*pS6K;
    R11f     : FourEBP1 => pFourEBP1                                ; Cell * MMWithKcat(k4Phos_km, k4EBP1Phos_kcat, FourEBP1, pmTORC1); 
    R11b     : pFourEBP1 => FourEBP1                                ; Cell * k4EBP1Dephos*pFourEBP1;
end
"""






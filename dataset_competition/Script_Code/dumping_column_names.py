# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:59:01 2017

@author: SERVER1
"""

import json

g_idx_cols = ['TimeLog', 'SPX', 'SSEC', 'GDAXI', 'N225', 'KOSPI', 'FCHI', 'BVSP', 'BSE', 'RTS', 'VNI']
g_idx2_cols = ['TimeLog', 'SPX', 'SHCOMP', 'NKY', 'DAX', 'KOSPI']

normal_idx_cols = ['TimeLog', 'bIXMLACWF', 'bIXMLWRLD', 'bIXMLEMKF', 'bIXMLEURO', 'bIXMLAAPF', 'bIXMLNAMR',
                'bIXNRCN', 'bIXNRUSDW', 'bIXMLEROP', 'bIXNRUK', 'bIXMLPACF', 'bIXNRAU', 'bIXNRHKHS', 'bIXNRJPTP',
                'bIXNRNZ', 'bIXNRSP', 'bIXMLEFLA', 'bIXNRAG', 'bIXNRCL', 'bIXNRMX', 'bIXMLEMEA', 'bIXNRSA',
                'bIXNRTK', 'bIXMLEMFA', 'bIXNRKOKS', 'bIXNRID', 'bIXNRMY', 'bIXNRPH', 'bIXNRTW', 'bIXNRTH']

kr_idx_cols = ['TimeLog', 'arKOBSNFKP', 'acKOFINBXDD', 'aaKOCIOO', 'afKOCIHPP0', 'afKOCIHJP0', 'afKOCIAJR0', 'arKOCIBSBP',
                'cCNNSKOPT', 'aoKOLWNUR', 'aaKOMBM2A', 'aaKOMBLFA', 'auKOMBRDB0', 'aaKOEIEX', 'aaKOEIIM', 'aaKOEIEXD',
                'aaKOEIIMD', 'bKOSMDM_YoY', 'bKOSMDM', 'bKODYKS', 'bKOIVVK', 'arKOIRCR', 'arKOIRKSDACD', 'arKOIRKSDATB3',
                'arKOIRKSDATB5', 'arKOIRKSDATB10', 'arKOIRKSDAMSB', 'arKOIRMSAAA3Y', 'arKOIRMFBAAA3Y', 'arKOIRMCPNAA33Y', 
               'arKOIRKSDATB5_YSR',  'arKOIRKSDATB10_YSR', 'arKOIRMSAAA3Y_YSR', 'arKOIRMFBAAA3Y_YSR',  'arKOIRMCPNAA33Y_YSR', 
               'ahKOPPDD', 'ahKOPPDD_YoY', 'cBKCFBLCL', 'aGLOCL6KOR', 'aKONA10RGDPGDP','aKONA10RGDPNA', 'aKONA10RGDPA', 
               'aKONA10RGDPC', 'aKONA10RGDPF', 'aKONA10RGDPS', 'aKONA10RGDPICT', 'aKONA10RGDPOICT', 'aKONA10RGDPPEI', 
               'aKONA10RGDPFI', 'aKONA10RGDPCC', 'aKONA10RGDPEG', 'aKONA10RGDPIG', 'aKONA10RGDPDDEI', 
                'aKONA10GRGNINGNI', 'aKONA10GRGNIRGNI', 'aKONA10GRGNIGDPDF', 'aKONA10GS', 'aKONA10GSGIR']

us_idx_cols = ['TimeLog', 'Auscbld_YoY', 'agUSMAIPTOTP', 'aqUSMAIUTOT', 'aUSBSISMPUR', 'aqUSBSCHBB', 'aqUSBSPHIM', 'aqUSBSISNBA',
                'aaUSMANOMDUR', 'aaUSMANOCPX', 'aqUSLWICUIC', 'aeUSLWECHNF', 'aeUSLWUR', 'aeUSPRCUSCONPRC', 'aeUSPRCXFDE', 'aeUSPRPFG',
               'aaUSWRSRX', 'abUSCE', 'aeUSMBSARDI', 'ahUSCSUMS', 'aqUSCSCF', 'aUSIRFDTRGD', 'aaUSMBM2', 'aUSIRTCM10D', 'aUSIRFRM30W', 
                'aUSIRFRM15W', 'aUSCIMGAI', 'aUSCIMGAIP', 'apUSCISESH', 'aeUSCISHNO', 'aaUSCISEMP', 'aaUSCISNMP', 'aeUSCIPH', 
               'aeUSCISTPH', 'aUSCINAHBMI', 'bIXSP25HOM', 'afUSCIOFSP10', 'aaUSEITB', 'aUSBSISMNO', 'aUSBSISMIV', 'aUSMBCACI', 
               'aaUSMBCO', 'aaUSMBCORE', 'abUSPI', 'abUSPIWS', 'abUSPIDIC', 'adUSPIDIC', 'aqUSBSISNON', 'arUSBSISNIO', 'aUSCBLD', 
               'aUSCBLD1', 'aUSCBLD2', 'aUSCBLD3', 'aUSCBLD5', 'aUSCBLD6', 'aUSCBLD8', 'aUSCBLD9', 'aUSCBLD10', 'aUSCBCO', 
               'aUSCBCO1', 'aUSCBCO2', 'aUSCBCO3', 'aUSCBCO4', 'aUSBSISMEM', 'aUSBSISMIM', 'aUSBSISMEO', 'aUSBSISMCP', 'aUSBSISMPR', 
               'aUSBSISMDL', 'aUSBSISMBO', 'aUSBSISMCI', 'bUSTIVIXPCMW', 'bUSTICBOEPCR', 'aUSIRMAAA1020D', 'aUSIRMBAA1020D']

cn_idx_cols = ['TimeLog', 'aGLOCL6CHN', 'aCHCBLD', 'apCHMAIP', 'aaCHWRRTT', 'aCHMBLFL', 'aCHPRCPI', 'aCHPRCPICR', 'aCHPRPPI', 
               'apCHMBM2YOY', 'aCHIRHSDT1Y', 'aCHMBRRR', 'aaCHEIEXM', 'aaCHEIIMM', 'aaCHEITBM', 'aaCHFIFDIUT', 'aCHNAGDYT', 'aaCHFIET', 
               'aCHBSPM', 'aCHMBM1GR', 'aCHCIRECI', 'aaCHCIRIYNI', 'aaCHBPCAC', 'aaCHBPCADE', 'aaCHBPG', 'aaCHBPGEX', 'aaCHBPGIM',
                'aaCHBPDIA', 'aaCHBPDIL', 'aCHEIEX', 'aCHEIIM', 'aCHPREX', 'aCHPRIM', 'aCHPRTT', 'aCHLWUEMP',
                'aCHCBCO', 'aCHCBLG', 'aCHCBSG', 'aCHBSBSIT', 'aCHCSCI', 'aCHCSSI', 'aCHCSEI', 'aCHMBRA',
                'aaCHMBM1', 'aaCHMBM2', 'aaCHMBM3', 'aCHMBM2GR', 'aCHIRDR', 'aCHIRIBO7D', 'aaCHFXFRM', 'aCHFXRUS',
                'apCHEGCNT', 'aCHEGSCCO', 'cpAMSACHT', 'cpAMSACHCAR']

de_idx_cols = ['TimeLog', 'agBDMANOT', 'agBDCIOCT', 'ahBDMAHS', 'aBDMANRC', 'abBDCE', 'aaBDBPCA', 'aaBDBPG', 'aaBDBPS', 'aaBDBPI', 
               'aaBDEIEX', 'aaBDEIIM', 'aaBDEITB', 'afBDPRC', 'afBDPRCN', 'afBDPRCCO', 'afBDPRP', 'afBDPREX', 'afBDPRIM', 
               'apBDLWUEM', 'aBDLWJV', 'arBDLWUR', 'afBDLWWI', 'aBDFXDEM', 'aaBDFXFR', 'aqBDBSIFOI', 'aqBDBSIFOP',
                'aqBDBSIFOR', 'arBDBSZEWRE', 'arBDBSZEWRB', 'arBDBSZEWPE', 'arBDBSZEWPB', 'aqBDCSCC', 'aGLIRPCEU', 'aGLOCL6DEU']


jp_idx_cols = ['TimeLog', 'afJPMAAL', 'agJPMAORM', 'ahJPMANRC', 'afJPCIST', 'afJPCISAT', 'afJPCISAON', 'afJPCISART', 'aaJPBPCA', 
               'aaJPBPG', 'aaJPEIEX', 'aaJPEIIM', 'afJPTINTT', 'afJPPRCNT', 'aJPCBLD', 'aJPCBCO', 'aJPCBLG', 'aJPCS', 'aJPBSTKA', 
               'aJPBSTKAM', 'aJPBSTKAMS', 'aJPBSTKANM', 'aJPBSTKANML', 'aJPBSTKF', 'aJPBSTKFM', 'aJPBSTKFNM', 'aaJPMBM1', 'aaJPMBM2', 
               'arJPFXER', 'aaJPPFSDQ', 'aaJPFSAIA', 'aGLIRPCJP', 'aGLOCL6JPN', 'aJPCBLD_YoY']

material_cols = ['TimeLog', 'aGLEGOFWTI', 'aGLEGOFBRT', 'aGLFUNG1', 'aGLFUXB1', 'aGLFUHO1', 'aGLRMLED3M', 'aGLRMLTI3M', 'aGLRMLZZ3M',
                'aGLRMLMEX', 'aGLRMLMEX', # Gold price
                'aGLFUSI1', 'aGLFUW1', 'aGLFUC1', 'aGLFUS1', 'aGLRMRR1', 'aGLFUSB1', 'aGLFUKC1', 'aGLFUJO1', 'aGLFULH1', 'aGLFULC1',
                'bIXMSW40R2', 'bIXMSEM40R2', 'aEUCIHPHF', 'aEUCIHPNW', 'aCHCIHPB', 'aCHCIHPT', 'aCHCIHPSH', 'aCHCIHPK', 'aCHCIHPSZ', 
                 'aGLREIDE', 'aGLREIMW', 'aGLREIMA', 'aGLREIME', 'aGLRMCRBGRNI', 'aGLRMNYFECRB', 'aGLRMCRBENGY', 'aGLRMCRBINDS', 
                 'aGLRMCRBPRMI', 'aGLFUCRY', 'Aglegofwti_YoY', 'aGLEGOFBRT_YoY', 'aGLFUNG1_YoY', 'aGLFUXB1_YoY', 'aGLFUHO1_YoY', 
                 'aGLRMLED3M_YoY', 'aGLRMLTI3M_YoY', 'aGLRMLZZ3M_YoY', 'aGLRMLMEX_YoY', 'aGLFUSI1_YoY', 'aGLFUW1_YoY', 'aGLFUC1_YoY', 
                 'aGLFUS1_YoY', 'aGLRMRR1_YoY', 'aGLFUSB1_YoY', 'aGLFUKC1_YoY', 'aGLFUJO1_YoY', 'aGLFULH1_YoY', 'aGLFULC1_YoY', 
                 'bIXMSW40R2_YoY', 'bIXMSEM40R2_YoY', 'aEUCIHPHF_YoY', 'aEUCIHPNW_YoY', 'aCHCIHPB_YoY', 'aCHCIHPT_YoY', 
                 'aCHCIHPSH_YoY', 'aCHCIHPK_YoY', 'aCHCIHPSZ_YoY', 'aGLREIDE_YoY', 'aGLREIMW_YoY', 'aGLREIMA_YoY', 'aGLREIME_YoY', 
                 'aGLRMCRBGRNI_YoY', 'aGLRMNYFECRB_YoY', 'aGLRMCRBENGY_YoY', 'aGLRMCRBINDS_YoY', 'aGLRMCRBPRMI_YoY',
                 'aGLFUCRY_YoY', 'aGLRMNRFTK', 'aGLRMPPRDRI']

exchange_cols = ['TimeLog', 'arKOFXUSDD', 'arKOFXJPYD', 'arKOFXEURD', 'arKOFXJPDD',
                'arKOFXDERD', 'arKOFXDUKD', 'arKOFXDAUD', 'arKOFXCNDD', 'arKOFXSWDD',
                'arKOFXHKDD', 'arKOFXTHDD', 'arKOFXINDD', 'afUSFXMCN', 'afUSFXBRI',
                'afUSFXOTN', 'afUSFXMCRR', 'afUSFXBRIR', 'afUSFXOTRR', 'arKOFXUSDD_YoY',
                'arKOFXJPYD_YoY', 'arKOFXEURD_YoY', 'arKOFXJPDD_YoY', 'arKOFXDERD_YoY',
                'arKOFXDUKD_YoY', 'arKOFXDAUD_YoY', 'arKOFXCNDD_YoY', 'arKOFXSWDD_YoY',
                'arKOFXHKDD_YoY', 'arKOFXTHDD_YoY', 'arKOFXINDD_YoY']

other_idx_cols = ['TimeLog','aGLOCL6OTO', 'aGLOCL6OEU', 'aGLOCL6ONM', 'aGLOCL6GBR', 'aGLOCL6FRA', 'aGLOCL6AUS', 'aGLOCL6MEX', 
                  'aTWCBLD', 'aGLOCL6IDN', 'aTHCBLD']


dic_colnames = {
    'G_IDX_CLOSE' : g_idx_cols,
    'G_IDX_HIGH' : g_idx_cols,
    'G_IDX_LOW' : g_idx_cols,
    'G_IDX_VOLUME' : g_idx_cols,
    'G_IDX_M_CAPITAL' : g_idx2_cols,
    'G_IDX_EPS' : g_idx2_cols,
    'G_IDX_PER' : g_idx2_cols,
    'NORMAL_IDX' : normal_idx_cols,
    'KR_INDEX' : kr_idx_cols,
    'US_INDEX' : us_idx_cols,
    'CN_INDEX' : cn_idx_cols,
    'DE_INDEX' : de_idx_cols,
    'JP_INDEX' : jp_idx_cols, 
    'MATERIALS' : material_cols,
    'EXCHANGES' : exchange_cols,
    'OTHER_IDX' : other_idx_cols
        }

fpath = 'C:/Users/SERVER1/bro.py/dataset_competition/'
with open(fpath+'colnames.json', 'w') as fp :
    json.dump(dic_colnames, fp)


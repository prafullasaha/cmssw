import FWCore.ParameterSet.Config as cms

def customise(process):
    if hasattr(process,'digitisation_step'):
        process=customise_Digi(process)
    if hasattr(process,'L1simulation_step'):
       process=customise_L1Emulator(process)
    if hasattr(process,'DigiToRaw'):
        process=customise_DigiToRaw(process)
    if hasattr(process,'RawToDigi'):
        process=customise_RawToDigi(process)
    if hasattr(process,'reconstruction'):
        process=customise_RecoFull(process)
    if hasattr(process,'famosWithEverything'):
        process=customise_RecoFast(process)
    if hasattr(process,'dqmoffline_step'):
        process=customise_DQM(process)
    if hasattr(process,'dqmHarvesting'):
        process=customise_harvesting(process)
    if hasattr(process,'validation_step'):
        process=customise_Validation(process)
    return process

def customise_Digi(process):
    process.RandomNumberGeneratorService.simMuonME0Digis = cms.PSet(
        initialSeed = cms.untracked.uint32(1234567),
        engineName = cms.untracked.string('HepJamesRandom')
    )

    process.mix.mixObjects.mixSH.crossingFrames.append('MuonME0Hits')
    process.mix.mixObjects.mixSH.input.append(cms.InputTag("g4SimHits","MuonME0Hits"))
    process.mix.mixObjects.mixSH.subdets.append('MuonME0Hits')

    process.load('SimMuon.GEMDigitizer.muonME0DigisPreReco_cfi')
    process.muonDigi += process.simMuonME0Digis

    process=outputCustoms(process)
    return process

def customise_L1Emulator(process):
    return process

def customise_DigiToRaw(process):
    return process

def customise_RawToDigi(process):
    return process

def customise_LocalReco(process):
    process.load('RecoLocalMuon.GEMRecHit.me0RecHits_cfi')
    process.load('RecoLocalMuon.GEMRecHit.me0Segments_cfi')
    
    process.me0RecHits.me0DigiLabel = cms.InputTag("simMuonME0Digis")
    process.me0Segments.me0RecHitLabel = cms.InputTag("me0RecHits")
    
    process.muonlocalreco += process.me0RecHits
    process.muonlocalreco += process.me0Segments
    return process

def customise_GlobalRecoInclude(process):
    process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAlong_cfi")
    process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorOpposite_cfi")
    process.load("TrackPropagation.SteppingHelixPropagator.SteppingHelixPropagatorAny_cfi")
    process.load('FastSimulation.Muons.me0SegmentProducer_cfi')
    process.load('RecoMuon.MuonIdentification.me0SegmentMatcher_cfi')
    process.load('RecoMuon.MuonIdentification.me0MuonConverter_cfi')
    return process
    
def customise_GlobalRecoFast(process):
    process.reconstructionWithFamos += process.me0SegmentProducer
    process.reconstructionWithFamos += process.me0SegmentMatcher
    process.reconstructionWithFamos += process.me0MuonConverter
    return process
    
def customise_GlobalRecoFull(process):
    process.reconstruction += process.me0SegmentProducer
    process.reconstruction += process.me0SegmentMatcher
    process.reconstruction += process.me0MuonConverter
    return process

def customise_RecoFast(process):
    process=customise_LocalReco(process)
    process=customise_GlobalRecoInclude(process)
    process=customise_GlobalRecoFast(process)
    process=outputCustoms(process)
    return process

def customise_RecoFull(process):
    process=customise_LocalReco(process)
    process=customise_GlobalRecoInclude(process)
    process=customise_GlobalRecoFull(process)
    process=outputCustoms(process)
    return process

def customise_DQM(process):
    return process

def customise_harvesting(process):
    return process

def customise_Validation(process):
    return process

def outputCustoms(process):
    alist=['AODSIM','RECOSIM','FEVTSIM','FEVTDEBUG','FEVTDEBUGHLT','RECODEBUG','RAWRECOSIMHLT','RAWRECODEBUGHLT']
    for a in alist:
        b=a+'output'
        if hasattr(process,b):
            getattr(process,b).outputCommands.append('keep *_simMuonME0Digis_*_*')
            getattr(process,b).outputCommands.append('keep *_me0RecHits_*_*')
            getattr(process,b).outputCommands.append('keep *_me0Segments_*_*')
            getattr(process,b).outputCommands.append('keep *_me0SegmentProducer_*_*')
            getattr(process,b).outputCommands.append('keep *_me0SegmentMatcher_*_*')
            getattr(process,b).outputCommands.append('keep *_me0MuonConverter_*_*')
    return process

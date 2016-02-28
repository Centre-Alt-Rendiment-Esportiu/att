# -*- coding: utf-8 -*-

import time

class ShortServiceProtocol:
    
    notifier = None
    view = None
    state = None
    currentState = None
    lastHit = None
    currentHit = None
    
    def __init__(self, view, notifier, state):
        self.view = view
        self.notifier = notifier
        self.state = state
    
    def processSate(self, hit):
        
        if self.currentState == None and self.lastHit == None:
            self.currentState = 1
            
        if self.currentState == 1:
            self.state.clear()
            self.currentHit = hit
            self.lastHit = None
            self.currentState = 2
            return
        
        if self.currentState == 2:
            self.lastHit = self.currentHit
            self.currentHit = hit
            
            time_delta = hit["tstamp"] - self.lastHit["tstamp"]
            self.notifier.push(str(time_delta))
            self.currentState = 1
            return
            

    
/*
 * Construction Intelligence Platform - Main Application
 * 
 * Copyright (c) 2025 Poor Dude Holdings LLC. All Rights Reserved.
 * PROPRIETARY AND CONFIDENTIAL - Unauthorized use prohibited.
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Navigation from './components/common/Navigation'
import ProjectRadar from './components/dashboard/ProjectRadar'
import OpportunityList from './components/dashboard/OpportunityList'
import Analytics from './components/dashboard/Analytics'
import CompetitorMap from './components/intelligence/CompetitorMap'
import RelationshipGraph from './components/intelligence/RelationshipGraph'
import DemandForecast from './components/pricing/DemandForecast'
import ScenarioAnalysis from './components/pricing/ScenarioAnalysis'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<ProjectRadar />} />
            <Route path="/opportunities" element={<OpportunityList />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/intelligence/competitors" element={<CompetitorMap />} />
            <Route path="/intelligence/relationships" element={<RelationshipGraph />} />
            <Route path="/pricing/forecast" element={<DemandForecast />} />
            <Route path="/pricing/scenarios" element={<ScenarioAnalysis />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App

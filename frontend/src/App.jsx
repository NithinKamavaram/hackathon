/**
 * Main CodeCollab Application
 */

import React, { useState, useEffect } from 'react';
import TaskSubmit from './components/TaskSubmit';
import AgentActivity from './components/AgentActivity';
import TaskList from './components/TaskList';
import StatusBar from './components/StatusBar';
import ResultDisplay from './components/ResultDisplay';
import * as api from './services/api';
import './styles/App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [currentTask, setCurrentTask] = useState(null);
  const [currentResult, setCurrentResult] = useState(null);
  const [agents, setAgents] = useState([
    { name: 'RequirementsAgent', status: 'idle', activity: 'Ready', progress: 0 },
    { name: 'ContextAgent', status: 'idle', activity: 'Ready', progress: 0 },
    { name: 'BuilderAgent', status: 'idle', activity: 'Ready', progress: 0 },
    { name: 'QualityAgent', status: 'idle', activity: 'Ready', progress: 0 },
    { name: 'EscalationAgent', status: 'idle', activity: 'Ready', progress: 0 }
  ]);
  const [systemStatus, setSystemStatus] = useState({
    status: 'loading',
    version: '1.0.0',
    agents_count: 5,
    swarm_available: false
  });
  const [error, setError] = useState('');

  // Load initial data
  useEffect(() => {
    loadSystemStatus();
    loadTasks();
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      loadSystemStatus();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const loadTasks = async () => {
    try {
      const taskList = await api.listTasks();
      setTasks(taskList);
    } catch (err) {
      console.error('Failed to load tasks:', err);
    }
  };

  const loadSystemStatus = async () => {
    try {
      const status = await api.getSystemStatus();
      setSystemStatus(status);
    } catch (err) {
      console.error('Failed to load status:', err);
    }
  };

  const handleTaskSubmitted = async (description, githubUrl = '', requirements = '') => {
    setError('');
    setCurrentResult(null); // Clear previous result

    // Simulate agent progression
    simulateAgentActivity();

    try {
      const result = await api.processTask(description, githubUrl, requirements);

      // Set current result for display
      setCurrentResult(result);

      // Add to task list
      setTasks(prev => [...prev, result]);

      // Update agents based on result
      if (result.agent_sequence) {
        updateAgentsFromResult(result);
      }

      // Reset after a delay
      setTimeout(() => {
        resetAgents();
      }, 2000);

      return result;
    } catch (err) {
      setError(err.message || 'Failed to process task');
      resetAgents();
      throw err;
    }
  };

  const simulateAgentActivity = () => {
    const sequence = [
      { name: 'RequirementsAgent', activity: 'Analyzing requirements...', delay: 0 },
      { name: 'ContextAgent', activity: 'Gathering context...', delay: 1000 },
      { name: 'BuilderAgent', activity: 'Writing code...', delay: 2000 },
      { name: 'QualityAgent', activity: 'Running tests...', delay: 3000 },
      { name: 'EscalationAgent', activity: 'Making decision...', delay: 4000 }
    ];

    sequence.forEach(({ name, activity, delay }) => {
      setTimeout(() => {
        setAgents(prev => prev.map(a =>
          a.name === name ? { ...a, status: 'working', activity, progress: 50 } : a
        ));
      }, delay);

      setTimeout(() => {
        setAgents(prev => prev.map(a =>
          a.name === name ? { ...a, status: 'completed', activity: 'Complete', progress: 100 } : a
        ));
      }, delay + 800);
    });
  };

  const updateAgentsFromResult = (result) => {
    setTimeout(() => {
      setAgents(prev => prev.map(agent => {
        if (result.agent_sequence?.includes(agent.name)) {
          return { ...agent, status: 'completed', activity: 'Complete', progress: 100 };
        }
        return agent;
      }));
    }, 5000);
  };

  const resetAgents = () => {
    setAgents([
      { name: 'RequirementsAgent', status: 'idle', activity: 'Ready', progress: 0 },
      { name: 'ContextAgent', status: 'idle', activity: 'Ready', progress: 0 },
      { name: 'BuilderAgent', status: 'idle', activity: 'Ready', progress: 0 },
      { name: 'QualityAgent', status: 'idle', activity: 'Ready', progress: 0 },
      { name: 'EscalationAgent', status: 'idle', activity: 'Ready', progress: 0 }
    ]);
  };

  const handleTaskClick = (task) => {
    setCurrentTask(task);
    setCurrentResult(task); // Show the clicked task's result
    console.log('Task clicked:', task);

    // Scroll to result display
    setTimeout(() => {
      const resultElement = document.querySelector('.result-display');
      if (resultElement) {
        resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 CodeCollab Swarm</h1>
        <p className="tagline">AI-Powered Development Assistant</p>
        <StatusBar status={systemStatus} />
      </header>

      {error && (
        <div className="error-banner">
          {error}
          <button onClick={() => setError('')}>×</button>
        </div>
      )}

      <main className="app-main">
        <div className="grid-layout">
          <div className="grid-left">
            <TaskSubmit onTaskSubmitted={handleTaskSubmitted} />
          </div>

          <div className="grid-right">
            <AgentActivity agents={agents} />
          </div>
        </div>

        {/* Display current task result */}
        {currentResult && (
          <div className="full-width">
            <ResultDisplay result={currentResult} />
          </div>
        )}

        <div className="full-width">
          <TaskList tasks={tasks} onTaskClick={handleTaskClick} />
        </div>
      </main>

      <footer className="app-footer">
        <p>Hack Midwest 2024 - Built with Strands SDK & Mock Swarm</p>
      </footer>
    </div>
  );
}

export default App;

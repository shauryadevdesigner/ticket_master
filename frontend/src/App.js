import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [events, setEvents] = useState([]);
  const [newEventUrl, setNewEventUrl] = useState('');
  const [notificationLog, setNotificationLog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Backend API URL - you'll need to update this with your deployed backend URL
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchEvents();
    fetchNotificationLog();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/events`);
      if (response.ok) {
        const data = await response.json();
        setEvents(data.events || []);
      }
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  const fetchNotificationLog = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/notifications`);
      if (response.ok) {
        const data = await response.json();
        setNotificationLog(data.log || []);
      }
    } catch (error) {
      console.error('Error fetching notification log:', error);
    }
  };

  const addEvent = async (e) => {
    e.preventDefault();
    if (!newEventUrl.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/events`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: newEventUrl }),
      });

      if (response.ok) {
        setNewEventUrl('');
        fetchEvents();
      }
    } catch (error) {
      console.error('Error adding event:', error);
    } finally {
      setLoading(false);
    }
  };

  const removeEvent = async (url) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/events`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (response.ok) {
        fetchEvents();
      }
    } catch (error) {
      console.error('Error removing event:', error);
    }
  };

  const sendNotification = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/notify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (response.ok) {
        setMessage('');
        fetchNotificationLog();
      }
    } catch (error) {
      console.error('Error sending notification:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎟️ Ticketmaster Ticket Tracker</h1>
        <p>Monitor your favorite events and get notified when tickets become available!</p>
      </header>

      <main className="App-main">
        {/* Notification Section */}
        <section className="notification-section">
          <h2>Send Test Notification</h2>
          <form onSubmit={sendNotification} className="notification-form">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Enter your notification message..."
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Sending...' : 'Send Notification'}
            </button>
          </form>
        </section>

        {/* Events Section */}
        <section className="events-section">
          <h2>Monitored Events</h2>
          <form onSubmit={addEvent} className="add-event-form">
            <input
              type="url"
              value={newEventUrl}
              onChange={(e) => setNewEventUrl(e.target.value)}
              placeholder="Enter Ticketmaster event URL..."
              required
            />
            <button type="submit" disabled={loading}>
              {loading ? 'Adding...' : 'Add Event'}
            </button>
          </form>

          <div className="events-list">
            {events.length === 0 ? (
              <p className="no-events">No events monitored yet. Add your first event above!</p>
            ) : (
              events.map((event, index) => (
                <div key={index} className="event-item">
                  <a href={event.url} target="_blank" rel="noopener noreferrer">
                    {event.url}
                  </a>
                  <span className="event-status">{event.status || 'Unknown'}</span>
                  <button
                    onClick={() => removeEvent(event.url)}
                    className="remove-btn"
                    disabled={loading}
                  >
                    Remove
                  </button>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Notification Log Section */}
        <section className="log-section">
          <h2>Recent Notifications</h2>
          <div className="notification-log">
            {notificationLog.length === 0 ? (
              <p className="no-notifications">No notifications sent yet.</p>
            ) : (
              notificationLog.map((log, index) => (
                <div key={index} className="log-item">
                  <div className="log-time">{log.timestamp}</div>
                  <div className="log-subject">{log.subject}</div>
                  <div className="log-message">{log.message}</div>
                </div>
              ))
            )}
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>
          <strong>Note:</strong> This frontend needs to be connected to a running backend API. 
          Make sure to set the <code>REACT_APP_API_URL</code> environment variable in Netlify 
          to point to your deployed backend.
        </p>
      </footer>
    </div>
  );
}

export default App;

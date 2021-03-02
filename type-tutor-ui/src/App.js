import './styles/App.scss';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Login from './scenes/Login';
import Register from './scenes/Register';
import MainPage from './scenes/MainPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/" exact component={MainPage} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;

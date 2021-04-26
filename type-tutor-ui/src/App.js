import './styles/App.scss';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Login from './scenes/Login';
import Register from './scenes/Register';
import UpdatePassword from './scenes/UpdatePassword';
import UpdateEmail from './scenes/UpdateEmail';
import DeleteAccount from './scenes/DeleteAccount';
import MainPage from './scenes/MainPage';
import Profile from './scenes/Profile';
import Navbar from './components/Navbar';
import Visualization from './scenes/Visualization';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Switch>
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <Route path="/update_password" component={UpdatePassword} />
          <Route path="/update_email" component={UpdateEmail} />
          <Route path="/delete_account" component={DeleteAccount} />
          <Route path="/profile" component={Profile} />
          <Route path="/" exact component={MainPage} />
          {/* <Route path="/visualization" exact component={Visualization} /> */}
        </Switch>
      </div>
    </Router>
  );
}

export default App;

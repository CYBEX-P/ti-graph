import React, { Component } from 'react'
import {BrowserRouter as Router, Route} from 'react-router-dom'

import Navbar from './components/Navbar'
import Landing from './components/Landing'
import Login from './components/Login'
import Register from './components/Register'
import Profile from './components/Profile'
import Find from './components/Find'
import Found from './components/Found'
import Remove from './components/Remove'
import Update from './components/Update'





class App extends Component {
  render() {
    return (
      <Router>
        <div className = "App">

      <Navbar/>
      <Route exact path ='/' component = {Landing} />
      <div className ="container">
      <Route exact path = '/register' component = {Register} />
      <Route exact path = '/login' component = {Login} />
      <Route exact path = '/profile' component = {Profile} />
      <Route exact path = '/remove' component = {Remove} />
      <Route exact path = '/update' component = {Update} />
      <Route exact path = '/find' component = {Find} />
      <Route exact path = '/found' component = {Found} />
      
      </div>
        </div>
      </Router>
      
    );
  }
}


export default App;

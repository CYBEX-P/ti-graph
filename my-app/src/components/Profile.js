import React, {Component} from 'react'
import jwt_decode from 'jwt-decode'

class Profile extends Component{
    constructor(){
        super()
        this.state ={
            username: '',
        
            errors: {}
            
        }
    }
    componentDidMount(){
        const token = localStorage.usertoken
        const decoded = jwt_decode(token)
        this.setState ({
            username: decoded.identity.username     
            
        })
    }
    render(){
        return(
            <div className = "container">
            <div className = "jumbotron mt-5">
            <div className = "col-sm-8 mt-5">
            <h1 className ="text-center">
            
            </h1>
            </div>
            <table className = "table col-md-6 mx-auto">
            <tbody>
                
                <tr>
                    <td>Username</td>
                    <td>{this.state.username}</td>
                </tr>
                
                
            </tbody>
            </table>
            </div>
            </div>
        )
    }
    
}

export default Profile
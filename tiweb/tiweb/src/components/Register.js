import React, {Component} from 'react'
import {register} from './UserFunctions'
//import CSRFToken from './csrf_token';
//import {withFetch} from 'fusion-plugin-csrf-protection-react';


class Register extends Component{
    constructor(){
        super()
        this.state = {
            first_name: '',
            last_name: '',
            email: '',
            username: '',
            password: ''
        }
        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }
    onChange(e){
        this.setState({[e.target.name]: e.target.value})
    }
    onSubmit(e){
        e.preventDefault()

        const newUser = {
            first_name: this.state.first_name,
            last_name: this.state.last_name,
            email: this.state.email,
            username: this.state.username,
            password: this.state.password 
        }

        register(newUser).then(res => {
            
                this.props.history.push('/login')
            
        })
    }

    render(){
        return (
            <div className = "container">
            <div className = "row">
            <div className = "col-md-6 mt-5 mx-auto">
            <form noValidate onSubmit = {this.onSubmit}>
            <h1 className = "h3 mb-3 font-weight-normal"> Register</h1>

            

            <div className = "form-group">
            <label htmlFor = "first_name"> First Name </label>
            <input type = "text"
            className = "form-control"
            name ="first_name" 
            placeholder = "Enter First Name"
            value = {this.state.first_name}
            onChange = {this.onChange}
            />
            </div>

            <div className = "form-group">
            <label htmlFor = "last_name"> Last Name </label>
            <input type = "text"
            className = "form-control"
            name ="last_name" 
            placeholder = "Enter Last Name"
            value = {this.state.last_name}
            onChange = {this.onChange}
            />
            </div>

            <div className = "form-group">
            <label htmlFor = "email"> Email Address </label>
            <input type = "email"
            className = "form-control"
            name ="email" 
            placeholder = "Enter email"
            value = {this.state.email}
            onChange = {this.onChange}
            />
            </div>

            <div className = "form-group">
            <label htmlFor = "username"> Username </label>
            <input type = "username"
            className = "form-control"
            name ="username" 
            placeholder = "Enter username"
            value = {this.state.username}
            onChange = {this.onChange}
            />
            </div>


            
            <div className = "form-group">
            <label htmlFor = "password"> Password </label>
            <input type = "password"
            className = "form-control"
            name ="password" 
            placeholder = "Enter password"
            value = {this.state.password}
            onChange = {this.onChange}
            />
            </div>
            <button type ="submit"
            className = "btn btn-lg btn-primary btn-block">
                Register
            </button>
            

            
            </form>
            </div>
            </div>
            </div>
        )
    }
}

export default Register
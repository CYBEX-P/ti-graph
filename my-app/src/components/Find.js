import React, {Component} from 'react'
import {find} from './UserFunctions'

class Find extends Component{
    constructor(){
        super()
        this.state = {
            username: '',
            
        }
        this.onChange = this.onChange.bind(this)
        this.onSubmit = this.onSubmit.bind(this)
    }
    onChange(e){
        this.setState({[e.target.name]: e.target.value})
    }
    onSubmit(e){
        e.preventDefault()

        const user = {
            username: this.state.username,
            
             
        }

        find(user).then(res => {
            
            console.log('found')
            
        
    })
    }

    render(){
        return (
            <div className = "container">
            <div className = "row">
            <div className = "col-md-6 mt-5 mx-auto">
            <form noValidate onSubmit = {this.onSubmit}>
            <h1 className = "h3 mb-3 font-weight-normal"> Find User</h1>

            

            <div className = "form-group">
            <label htmlFor = "first_name"> First Name </label>
            <input type = "text"
            className = "form-control"
            name ="username" 
            placeholder = "Enter Username"
            value = {this.state.username}
            onChange = {this.onChange}
            />
            </div>

            <button type ="submit"
            className = "btn btn-lg btn-primary btn-block">
                
                
                Find
            </button>

            
            
            </form>
            </div>
            </div>
            </div>
        )
    }
}

export default Find
import React, {Component} from 'react'
import {remove} from './UserFunctions'

class Remove extends Component{
    constructor(){
        super()
        this.state = {
            username: ''
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

        remove(user).then(res => {
            
            //this.props.history.push('/login')
            console.log('deleted')
        
    })
    }

    render(){
        return (
            <div className = "container">
            <div className = "row">
            <div className = "col-md-6 mt-5 mx-auto">
            <form noValidate onSubmit = {this.onSubmit}>
            <h1 className = "h3 mb-3 font-weight-normal"> Delete</h1>

            

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
                Delete
            </button>

            
            
            </form>
            </div>
            </div>
            </div>
        )
    }
}

export default Remove
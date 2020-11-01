import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent implements OnInit {
  query: string;
  
  constructor(private router: Router) {}

  ngOnInit() {}
  
  onQuery() {
    this.router.navigate(['/search'], { queryParams: {query: this.query} });
  }

}

import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css'],
})
export class HeaderComponent {
  constructor(private router: Router) {}

  RouteToHomePage() {
    this.router.navigate(['/']);
  }

  RouteToGuidePage() {
    this.router.navigate(['guide']);
  }

  RouteToAlgorithmsPage() {
    this.router.navigate(['algorithms']);
  }
}

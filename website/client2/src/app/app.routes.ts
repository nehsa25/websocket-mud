import { Routes } from '@angular/router';
import { MudComponent } from './main/mud/mud.component';

export const routes: Routes = [
  { path: 'mud', title: 'nehsa.net | MUD', component: MudComponent },
  { path: '**', component: MudComponent }, // Default route if nothing else found
];

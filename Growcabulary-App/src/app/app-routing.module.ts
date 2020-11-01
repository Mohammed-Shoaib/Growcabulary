import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { WordDetailComponent } from './word-detail/word-detail.component';
import { PriceDetailComponent } from './price-detail/price-detail.component';
import { AboutComponent } from './about/about.component';
import { WordListComponent } from './word-list/word-list.component';
import { WordSearchComponent } from './word-search/word-search.component';


const routes: Routes = [
  { path: 'learn/:folder', component: WordListComponent },
  { path: 'learn', component: WordDetailComponent },
  { path: 'pricing', component: PriceDetailComponent },
  { path: 'about', component: AboutComponent },
  { path: 'search', component: WordSearchComponent },
  { path: '', redirectTo: 'learn', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

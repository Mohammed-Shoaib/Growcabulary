import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Word } from '../word.model';
import { WordListService } from '../word-list.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-word-search',
  templateUrl: './word-search.component.html',
  styleUrls: ['./word-search.component.scss']
})
export class WordSearchComponent implements OnInit {
  results: Word[];
  subscription: Subscription;
  
  constructor(private route: ActivatedRoute, private router: Router, private wordListService: WordListService) {}

  ngOnInit(): void {
    this.subscription = this.route.queryParams.subscribe(queryParams => {
      if (!queryParams.hasOwnProperty('query') || queryParams.query.length === 0)
        this.router.navigate(['/']);
      this.results = this.wordListService.searchQuery(queryParams.query);
    });
  }
  
  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
  
  cardClick(index: number) {
    let key = this.results[index].key;
    let word = this.wordListService.getWord(key);
    this.router.navigate(['/learn', word.folderName], { queryParams: {index: word.index} });
  }

}

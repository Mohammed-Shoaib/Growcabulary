import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { WordListService } from '../word-list.service';

@Component({
  selector: 'app-word-detail',
  templateUrl: './word-detail.component.html',
  styleUrls: ['./word-detail.component.scss']
})
export class WordDetailComponent implements OnInit {
  constructor(private router: Router, public wordListService: WordListService) { }

  ngOnInit(): void {}
  
  getLevelIndexes(level: string) {
    let levelIndexes = [];
    this.wordListService.folders.forEach((folder, i) => {
      if (folder.split(' ')[0] === level)
        levelIndexes.push(i);
    });
    return levelIndexes;
  }
}

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvalidNameComponent } from './invalid-name.component';

describe('InvalidNameComponent', () => {
  let component: InvalidNameComponent;
  let fixture: ComponentFixture<InvalidNameComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InvalidNameComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InvalidNameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
